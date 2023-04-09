from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_mail import Mail, Message
from src.models import db
from dotenv import load_dotenv
from src.repositories.user_repository import user_repository_singleton
import os
load_dotenv()

app = Flask(__name__)
file = open("user.txt", "a")



curr_user = -1


#DB connection
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DBNAME')
print(db_name)
app.config['SQLALCHEMY_DATABASE_URI']\
      =  f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)
print("HERE")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gregslist.customer.service@gmail.com'
app.config['MAIL_PASSWORD'] = 'yisphiuewbsczkuq'
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
    file = open("user.txt", "r")
    curr_user = file.read()
    file.close()
    my_user = user_repository_singleton.get_user_by_id(curr_user)

    hour = datetime.now().hour
    if hour < 11:
        time_of_day = "Morning"
    elif hour >= 11 and hour < 17:
        time_of_day = "Afternoon"
    else:
        time_of_day = "Evening"
    print(curr_user)
    print("MADE IT HERE")

    first_name = my_user.first_name
    first_name = first_name.title()
    last_name = my_user.last_name
    last_name = last_name.title()
    username = my_user.username
    password = my_user.user_password
    email = my_user.user_email
    return render_template('my_account.html', first_name = first_name, last_name = last_name, username = username, password = password, email = email, time_of_day = time_of_day)

#TODO
#fix the return once page is made
@app.get('/sign_in')
def sign_in():
    file = open("user.txt", "r")
    curr_user = file.read()
    file.close()
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

#NOTE need to add a connection between flask and html form following the week of 3/29/23



# create user signup page
@app.get('/signup')
def signup_page():
    file = open("user.txt", "r")
    curr_user = file.read()
    file.close()
    if curr_user != "":
        return render_template('home.html')
    return render_template('signup.html')

@app.post('/signup')
def signup_form():
    new_fname = str(request.form.get('fname'))
    new_lname = str(request.form.get('lname'))
    new_email = str(request.form.get('email'))
    new_user = str(request.form.get('username'))
    new_pass = str(request.form.get('user_pass'))


    #checks to make sure user does not already exist.
    if not(user_repository_singleton.validate_user(new_user)):
        print("Looks safe!")
        curr_user = user_repository_singleton.add_user(new_fname, new_lname, new_user, new_pass, new_email).user_id
        file = open("user.txt", "a")
        file.seek(0)
        file.truncate()
        file.write(str(curr_user))
        file.close()
        user_repository_singleton.change_email( curr_user, "qwertyuiop", new_user, new_pass)
       
        return redirect('/my_account')
    else:
        file = open("user.txt", "r")
        curr_user = file.read()
        file.close()
        return redirect('/sign_in')