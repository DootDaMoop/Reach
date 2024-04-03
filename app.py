from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/calendar')
def calendar():
    return render_template('calendar.html')