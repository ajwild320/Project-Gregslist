from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('home.html')

@app.get('/contact_us')
def contact_us():
    return render_template('contact_us.html')