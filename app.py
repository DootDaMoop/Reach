from flask import Flask, render_template
from flask import request
#from model.User import User
class user:
    first_name = 'Connor'
    last_name = 'Ayscue'
    username = 'ConnorAsq'
    password = '123456789'
    instagram = 'Connor_asku'
    snapchat = ''
    email = 'connorjayscue@gmail.com'

app = Flask(__name__)

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

#@app.get('/edit')
#def profile():
#    user.first_name = request.form.get('first_name')
#    user.last_name = request.form.get('last_name')
#    full_name = user.first_name + ' ' + user.last_name

#    user.username = request.form.get('username')
#    user.password = request.form.get('password')
#    user.email = request.form.get('email')

#    user.snapchat = request.form.get('snapchat')
#    user.instagram = request.form.get('instagram')

#    return render_template('eidt_profile.html', user=user, full_name=full_name)