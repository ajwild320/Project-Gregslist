from flask import Flask, render_template, request, redirect

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
    first_name = "a"
    first_name = first_name.title()
    last_name = "b"
    last_name = last_name.title()
    username = "c"
    password = "d"
    email = "e"
    return render_template('my_account.html', first_name = first_name, last_name = last_name, username = username, password = password, email = email)

#TODO
#fix the return once page is made
@app.get('/sign_in')
def sign_in(username, password):
    return render_template('home.html')