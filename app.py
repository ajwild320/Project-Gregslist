from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gregslist.customer.service@gmail.com'
app.config['MAIL_PASSWORD'] = 'qcjzwfmmyaekkcgt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

#with the new information learned in class on 3/28/2023 we should be able to create
#and populate the database with the new information needed to implement the sign in
#feature
@app.get('/my_account_invalid')
def my_account_invalid():
    username = request.form.get('username')
    password = request.form.get('password')
    return render_template('my_account_invalid.html')

#TODO
#retrieve from when a user is created

#can use database to check if a user exists
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

# can also assign ID's to each user account and delete them via ID
@app.get('/deactivate_account')
def deactivate_account():
    return render_template('deactivate_account.html')

@app.get('/report_post')
def report_post():     
    return render_template('report_post.html')

#TODO
#update to take sender and cc as user, return an error page if doesnt work
@app.post('/report_post_email')
def report_post_email():
    msg = Message('Report Post', sender = 'gregslist.customer.service@gmail.com', cc = ['gregslist.customer.service@gmail.com'], recipients = ['gregslist.customer.service@gmail.com'])
    msg.body = request.form.get("reason")
    mail.send(msg)
    return render_template('home.html')
