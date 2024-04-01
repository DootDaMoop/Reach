from flask import Flask, render_template
from model.User import User

app = Flask(__name__)

user = User()

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/calendar')
def calendar():
    return render_template('calendar.html')

@app.get('/profile')
def profile():
    full_name = user.first_name + ' ' + user.last_name
    return render_template('profile.html', user=user, full_name=full_name)

@app.get('/edit')
def profile():
    
    return render_template('eidt_profile.html', user=user, full_name=full_name)