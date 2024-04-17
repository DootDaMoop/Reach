import os
import pathlib
import requests
import json
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from model.User import User
from user_repo.User_management import User_management
from dotenv import load_dotenv
from repositories import user_repo, group_repo, event_repo
from functools import wraps

load_dotenv()

app = Flask(__name__)

# user = User()
# user_management = User_management(r"user_repo\users.csv")

with open('client_secrets.json', 'r') as file:
    config = json.load(file)

    client_id = config['web']['client_id']
    project_id = config['web']['project_id']
    auth_uri = config['web']['auth_uri']
    token_uri = config['web']['token_uri']
    auth_provider_x509_cert_url = config['web']['auth_provider_x509_cert_url']
    client_secret = config['web']['client_secret']
    redirect_uris = config['web']['redirect_uris']

app.secret_key = client_secret

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_ID = client_id
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client_secrets.json')

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri='http://127.0.0.1:5000/callback'
)


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.get('/google_login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


@app.get('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session['state'] == request.args['state']:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=300
    )
    
    session['first_name'] = id_info.get('given_name')
    session['last_name'] = id_info.get('family_name')
    session['email'] = id_info.get('email')
    session['pfp'] = id_info.get('picture')
    session['google_id'] = id_info.get('sub')
    session['user_name'] = id_info.get('name')

    if not user_repo.user_exists(id_info.get('name')):
        user_repo.register_user(id_info.get('name'), id_info.get('email'), None, id_info.get('given_name'),id_info.get('family_name'), id_info.get('sub'))
    
    user = user_repo.get_user_from_username(id_info.get('name'))
    session['user_id'] = user['user_id']
    return redirect('/home')

# TODO: If you want to log out, just localhost://logout in your url, implement logout button on homepage later.
@app.get('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/registration')
def registration():
    return render_template('registration.html')

@app.get('/calendar')
def calendar():
    return render_template('calendar.html')


@app.post('/register')
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    if not password == confirm_password:
        return 'Passwords do not match. Please try again.', 400
    
    success, message = user_repo.register_user(username, email, password, first_name, last_name, None)

    if success:
        return redirect('/')
    else:
        return message, 400

    

@app.post('/login_manual')
def login_manual():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    validated = user_repo.validate_user(username, email, password)

    if validated:
        user = user_repo.get_user_from_username(username)

        session['user_id'] = user['user_id']
        session['email'] = user['user_email']
        session['first_name'] = user['user_first_name']
        session['last_name'] = user['user_last_name']
        session['pfp'] = None
        session['google_id'] = None
        session['user_name'] = user['user_name']

        return redirect('/home')
    else:
        return 'Invalid email or password. Please try again.', 400

#the page you land after you log in 
@app.get('/home')
@login_is_required
def home():
    cur_user_groups = group_repo.get_user_groups_from_user_id(session['user_id'])
    return render_template("home.html", cur_user_groups=cur_user_groups)

@app.get('/profile/<int:user_id>')
def profile(user_id: int):
    user = user_repo.get_user_from_user_id(user_id)
    return render_template('profile.html', user=user)

@app.get('/profile/<int:user_id>/edit')
def get_edit_user_profile_page(user_id: int):
    if session['user_id'] == user_id:
        user = user_repo.get_user_from_user_id(session['user_id'])
        return render_template('edit_profile.html', user=user)
    else:
        return 'Unauthorized Access', 401

@app.post('/profile/<user_id>/edit')
def edit_user_profile(user_id: int):
    user = user_repo.get_user_from_user_id(session['user_id'])
    new_user = user_repo.edit_user(user['user_id'], request.form.get('username'), request.form.get('email'), request.form.get('password'), request.form.get('first_name'), request.form.get('last_name'))
    return redirect(f"/profile/{user_id}")

@app.get('/groups/create/')
@login_is_required
def get_create_group_page():
    return render_template('create_group.html')

@app.post('/groups/create/')
def create_group_page():
    group_name = request.form.get('group_name')
    group_description = request.form.get('group_description')
    group_public = request.form.get('is_group_public')

    if group_name is None or group_description is None:
        return 'Invalid Group Name or Group Description', 400

    if group_public is not None:
        group_public = True
    else:
        group_public = False

    success, message = group_repo.create_group(session['user_id'], group_name, group_description, group_public)
    
    if success:
        return redirect('/home')
    else:
        return message, 400

if __name__ == "__main__":
    app.run(debug=True)