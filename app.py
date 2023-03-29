from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('home.html')

#TODO
#Get the items and send them in an email to admin account
@app.get('/contact_us')
def contact_us():
    return render_template('contact_us.html')

#TODO
#needs to be finished once the sign in is completed and we know where to redirect to
@app.get('/my_account_invalid')
def my_account_invalid():
    username = request.form.get('username')
    password = request.form.get('password')
    return render_template('my_account_invalid.html')

#TODO
#retrieve from when a user is created
@app.get('/my_account')
def my_account():
    hour = datetime.now().hour
    if hour < 11:
        time_of_day = "Morning"
    elif hour >= 11 and hour < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"

    first_name = "a"
    first_name = first_name.title()
    last_name = "b"
    last_name = last_name.title()
    username = "c"
    password = "d"
    email = "e"
    return render_template('my_account.html', first_name = first_name, last_name = last_name, username = username, password = password, email = email, time_of_day = time_of_day)

#TODO
#fix the return once page is made
@app.get('/sign_in')
def sign_in(username, password):
    return render_template('home.html')

#TODO
#once database is created, use the username to delete from database
@app.get('/deactivate_account')
def deactivate_account():
    return render_template('deactivate_account.html')

#TODO
#will need to implement how to send this data to an email
@app.get('/report_post')
def report_post():     
    return render_template('report_post.html')

#TODO
#need to update once it is figured out how to send a form via email
@app.post('/report_post_email')
def report_post_email():
    return render_template('home.html')
