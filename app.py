import os
import pathlib
import requests
import json
from flask import Flask, session, abort, redirect, request, render_template, url_for, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from dotenv import load_dotenv
from repositories import user_repo, group_repo, event_repo, email_repo
from functools import wraps
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)

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

    if not user_repo.user_exists(id_info.get('name'), id_info.get('email')):
        user_repo.register_user(id_info.get('name'), id_info.get('email'), None, id_info.get('given_name'),id_info.get('family_name'), id_info.get('sub'))
    
    user = user_repo.get_user_from_user_email(id_info.get('email'))
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
    session['prev_url'] = url_for('home')
    groups = group_repo.get_groups_from_user_id(session['user_id'])
    home_events = event_repo.get_all_user_group_events(session['user_id'])
    return render_template("home.html", groups=groups, home_events=home_events, verify_admin_user=event_repo.verify_user_admin_for_event)

#the page if you click on a group
@app.get('/groups/<int:group_id>/')
def group(group_id: int):
    session['prev_url'] = url_for('group', group_id=group_id)
    group = group_repo.get_user_group_from_group_id(group_id) # indiviudal group instance of selected element
    member_count = group_repo.get_member_count_from_group_id(group_id) # selcted group's member count
    group_owner = group_repo.get_group_and_user_from_group_id(group_id) # returns joint table between user-membership-group 

    members = group_repo.get_members_from_group_id(group_id)
    membership = group_repo.get_role_in_group_from_user_and_group_id(session['user_id'], group_id) # Get user's role in group
    group_events = event_repo.get_all_user_group_events_for_selected_group(session['user_id'], group_id) # Gets all events from group that user has been pending(invited) to.
    
    # Everything above this comment is information for the indvidual selected group
    sidebar_groups = group_repo.get_groups_from_user_id(session['user_id'])
    return render_template('group.html', group=group, sidebar_groups=sidebar_groups, group_owner=group_owner, member_count = member_count, membership=membership, group_events=group_events, members=members)

@app.post('/groups/<int:group_id>/join')
def group_join(group_id: int):
    if(group_repo.check_membership(session['user_id'], group_id) is None): # checks if user is member, if not then add them to group
        group_repo.join_group(session['user_id'], group_id)        
    return redirect(url_for('group', group_id=group_id))

@app.post('/groups/<int:group_id>/leave')
def group_leave(group_id: int):
    if(group_repo.check_membership(session['user_id'], group_id) is not None): # checks if the user exist, if so remove them
        group_repo.remove_member_from_group(session['user_id'], group_id)    
        
    member_count = group_repo.get_member_count_from_group_id(group_id) # member count of group 
    if(member_count == 0):
        group_repo.delete_group(group_id) # deletes a group from database if member count is 0
    return redirect('/home') # redirect to home page

@app.get("/groups/<group_id>/group_edit/")
def edit(group_id: str):
    members = group_repo.get_members_from_group_id(group_id)
    group = group_repo.get_user_group_from_group_id(group_id)
    return render_template("group_edit.html", members=members, group=group)


@app.post('/accept_event')
def accept_event():
    data = request.json
    event_id = data['eventId']
    user_id = data['userId']

    if not event_id or not user_id:
        return jsonify({'error': 'missing eventId or userId'}), 400
    
    if int(user_id) != session['user_id']:
        return jsonify({'error': 'Unauthorized user'}), 401
    
    event_repo.accept_event(event_id, user_id)

    return jsonify({'message': 'Event accepted successfully'})

@app.post('/decline_event')
def decline_event():
    data = request.json
    event_id = data['eventId']
    user_id = data['userId']

    if not event_id or not user_id:
        return jsonify({'error': 'missing eventId or userId'}), 400
    
    if int(user_id) != session['user_id']:
        return jsonify({'error': 'Unauthorized user'}), 401
    
    event_repo.decline_event(event_id, user_id)

    return jsonify({'message': 'Event declined successfully'})

@app.post('/revert_event')
def revert_event():
    data = request.json
    event_id = data['eventId']
    user_id = data['userId']

    if not event_id or not user_id:
        return jsonify({'error': 'missing eventId or userId'}), 400
    
    if int(user_id) != session['user_id']:
        return jsonify({'error': 'Unauthorized user'}), 401
    
    event_repo.revert_event_choice(event_id, user_id)

    return jsonify({'message': 'Event declined successfully'})

@app.post('/get_num_events_for_day')
def get_user_events_for_calendar_on_day():
    data = request.json
    year = data['year']
    month = data['month']
    day = data['day']

    events = event_repo.get_user_events_for_day(session['user_id'],year, month, day)

    return jsonify(events)


@app.get('/groups/<int:group_id>/group_edit/')
def get_edit_group_page(group_id: int):
    if group_repo.get_role_in_group_from_user_and_group_id(session['user_id'], group_id)['user_role'] != (0 and 1):
        return redirect(url_for('get_edit_group_page', group_id=group_id))

    members = group_repo.get_members_from_group_id(group_id)
    group = group_repo.get_user_group_from_group_id(group_id)
    
    
    return render_template("group_edit.html", members=members, group=group)

@app.post("/groups/<group_id>/group_edit/")
def save_group_edit_changes(group_id: str):
    group_name = request.form.get('group-name')
    group_description = request.form.get('description')
    group_publicity = request.form.get('privacy') # grabs checkbox
    print(group_publicity)
    if(group_publicity is None): # if checkbox is blank, privacy is public --> true
        group_publicity = True
    elif(group_publicity == "on"):
        group_publicity = False
    
    # TODO: CALL GROUP REPO METHODS TO UPDATE DATA INTO DATABASE
    group_repo.update_group(group_id, group_name, group_description, group_publicity) # updates group
    return redirect(url_for('edit', group_id=group_id))

@app.get('/groups/<int:group_id>/create_event/')
def get_create_event_page(group_id:int):
    authorized_user_role = group_repo.get_role_in_group_from_user_and_group_id(session['user_id'], group_id)['user_role']
    if authorized_user_role != 0 and authorized_user_role != 1:
        return redirect(url_for('group', group_id=group_id))
    
    group = group_repo.get_user_group_from_group_id(group_id)
    return render_template('create_event.html', group=group)

@app.post('/groups/<int:group_id>/create_event/')
def create_event_for_selected_group(group_id: int):
    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    event_public = request.form.get('is_event_public')
    event_start_date = request.form.get('event_start_date')
    event_end_date = request.form.get('event_end_date')

    if any(value is None or value == '' for value in [event_name, event_description, event_start_date, event_end_date]):
        return redirect(url_for('get_create_event_page', group_id=group_id)) # TODO: Error Message!
    
    if event_public is None:
        event_public = False

    event = event_repo.create_event(session['user_id'],group_id, event_name, event_description, event_public, event_start_date, event_end_date)

    # If an event is public then all the users in a group will be invited.
    if event['event_public']:
        event_repo.invite_all_users_in_group_to_event(group_id, event['event_id'])
    else:
        event_repo.invite_user_to_event(session['user_id'], event['event_id'])
        group = group_repo.get_group_by_id(group_id)
        if session['user_id'] != group['user_id']:
            event_repo.invite_user_to_event(group['user_id'],event['event_id'])

    return redirect(f'/groups/{group_id}/')

@app.get('/groups/<int:group_id>/event_edit/<int:event_id>/')
def get_event_edit_page(group_id: int, event_id: int):
    session['event_id'] = event_id
    session['group_id'] = group_id
    group = group_repo.get_user_group_from_group_id(group_id)
    event = event_repo.get_event_by_event_id(event_id)
    members = event_repo.get_members_for_edit_event_page(group_id)
    return render_template('edit_event.html', group=group, event=event, members=members, verify_member_is_invited_to_event=event_repo.verify_member_is_invited_to_event, get_attending_status=event_repo.get_attending_status)

@app.post('/groups/<int:group_id>/event_edit/<int:event_id>/')
def update_edited_event(group_id: int, event_id: int):
    if event_id != session['event_id'] or group_id != session['group_id']:
        return redirect(url_for('get_event_edit_page', group_id=session['group_id'], event_id=session['event_id']))

    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    event_public = request.form.get('is_event_public')
    event_start_date = request.form.get('event_start_date')
    event_end_date = request.form.get('event_end_date')

    if any(value is None or value == '' for value in [event_name, event_description, event_start_date, event_end_date]):
        return redirect(url_for('get_event_edit_page', event_id=session['event_id'])) # TODO: Error Message

    if event_public is None:
        event_public = False

    event_repo.edit_event(event_id, event_name, event_description, event_public, event_start_date, event_end_date)

    return redirect(url_for('get_event_edit_page', group_id=group_id, event_id=event_id))

@app.post('/groups/<int:group_id>/event_edit/<int:event_id>/delete/')
def delete_event(event_id: int, group_id: int):
    if event_id != session['event_id'] or group_id != session['group_id']:
        return redirect(url_for('get_event_edit_page', group_id=session['group_id'], event_id=session['event_id']))
    
    event = event_repo.get_event_by_event_id(event_id)

    # If the event is false, and the user's who made the event is not the logged in user or the owner of the group.
    if event['event_public'] is False and (event['user_id'] != session['user_id'] or group_repo.get_user_group_from_group_id(event['group_id'])['user_id'] != session['user_id']):
        return redirect(url_for('get_event_edit_page', group_id=group_id, event_id=event_id))
    
    event_repo.delete_event(event_id)
    print(session['prev_url'])
    return redirect(session['prev_url'])

@app.get('/groups/<int:group_id>/group_edit/delete/')
def delete_individual_group(group_id: int):

    #Make sure user is owner of group to delete 
    if group_repo.get_role_in_group_from_user_and_group_id(session['user_id'], group_id)['user_role'] != (0):
        return redirect(url_for('get_edit_group_page', group_id=group_id))
    
    group_repo.delete_group(group_id)
    
    return redirect('/home')

#PROFILE ROUTES



@app.post('/invite_to_event')
def invite_to_event():
    data = request.json
    event_id = data['eventId']
    user_id = data['userId']

    if not event_id or not user_id:
        return jsonify({'error': 'missing eventId or userId'}), 400
    
    event_repo.invite_user_to_event(user_id, event_id)

    return jsonify({'message': 'User invited successfully'})

@app.post('/remove_invite_to_event')
def remove_invite_to_event():
    data = request.json
    event_id = data['eventId']
    user_id = data['userId']

    if not event_id or not user_id:
        return jsonify({'error': 'missing eventId or userId'}), 400
    
    event_repo.remove_invited_user_from_event(user_id, event_id)
    print('deleted user invite')

    return jsonify({'message': 'User Invite Removed successfully'})

@app.get('/profile/<int:user_id>')
def profile(user_id: int):
    user = user_repo.get_user_from_user_id(user_id)

    return render_template('profile.html', user=user)

@app.get('/profile/<int:user_id>/edit/')
def get_edit_user_profile_page(user_id: int):
    if session['user_id'] == user_id:
        user = user_repo.get_user_from_user_id(session['user_id'])
        return render_template('edit_profile.html', user=user)
    else:
        return 'Unauthorized Access', 401

@app.post('/profile/<int:user_id>/edit/')
def edit_user_profile(user_id: int):
    if user_id != session['user_id']:
        print("NO HACKING")
        return redirect(url_for(get_edit_user_profile_page, user_id=session['user_id']))
    
    user = user_repo.get_user_from_user_id(session['user_id'])
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    if any(value is None or value == '' for value in [username, email]):
        return redirect(url_for('get_edit_user_profile_page', user_id=session['user_id'])) # TODO: Error Message

    profile_picture = user_repo.update_profile_picture(session['user_id'], request.files.get('profile_picture')) # TODO: Add separate var for pfp and combine to main update function
    user_repo.edit_user(user['user_id'], username, email, password, first_name, last_name)

    return redirect(url_for('get_edit_user_profile_page', user_id=session['user_id']))

@app.get('/event_picture/<int:event_id>')
def event_picture(event_id):
    return event_repo.get_event_picture(event_id)

@app.get('/profile_picture/<int:user_id>')
def profile_picture(user_id):
    return user_repo.get_profile_picture(user_id)

@app.get('/group_picture/<int:group_id>')
def group_picture(group_id):
    return group_repo.get_group_picture(group_id)

@app.post('/profile/<int:user_id>/edit/delete')
def delete_user_profile(user_id: int):
    if user_id != session['user_id']:
        return redirect(url_for(get_edit_user_profile_page, user_id=session['user_id']))
    
    #get list of groups that contain groups owned by user
    owned_groups = group_repo.get_user_groups_from_user_id(user_id) 

    #If user is not the owner of any groups
    if owned_groups is None:
        user_repo.delete_user(session['user_id'])
    else: 
        #for users that own groups, transfer status to an admin
        for group in owned_groups:

            #grab an admin to make the new owner of the group
            new_owner = group_repo.get_admin_member_and_role(group['group_id'])

            #makes sure list of admins is not empty
            if type(new_owner) is int:
                #get user_id of new owner
                new_owner_id = new_owner['user_id']

                #change user role to owner
                group_repo.change_member_role(new_owner_id, group['group_id'], 0)

            #if the admin list is empty just delete the group
            else:
                #Delete group
                group_repo.delete_group(group['group_id'])
        
        user_repo.delete_user(session['user_id'])

    return redirect('/logout')




@app.get('/groups/create/')
@login_is_required
def get_create_group_page():
    return render_template('create_group.html')

@app.get('/find_group')
def load_find_group_page():
    groups = group_repo.all_groups()
    return render_template('find_group.html', groups=groups)

@app.post('/groups/create/')
@login_is_required
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
    
@app.get('/event') 
def event():
    return render_template("event.html")

if __name__ == "__main__":
    app.run(debug=True)
