from flask import Flask, render_template, request, redirect, abort
from datetime import datetime
from flask_mail import Mail, Message
from src.models import db, Item
from src.repositories.item_repository import item_repository_singleton
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

#DB connection
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI']\
    = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

db.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
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
#More suitable for a nonexisting user as some data could be pulled from database
@app.post('/contact_us_email')
def contact_us_email():
    name = request.form.get("name")
    email = request.form.get("email")
    reason = request.form.get("reason")
    if name.__len__() == 0 or email.__len__() == 0 or reason.__len__() == 0:
        return redirect('/contact_us')
    else:
        subject_line = "{} is reaching out".format(name)
        body = "{} is reaching out. They can be responded to at {}. They are reaching out in regards of: {}".format(name, email, reason)
        msg = Message(subject_line, sender = 'gregslist.customer.service@gmail.com', recipients = ['gregslist.customer.service@gmail.com', email])
        msg.body = body
        mail.send(msg)
        return render_template('home.html')

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
#update to send user as a recipient, return an error page if doesnt work
@app.post('/report_post_email')
def report_post_email():
    msg = Message('Report Post', sender = 'gregslist.customer.service@gmail.com', recipients = ['gregslist.customer.service@gmail.com'])
    msg.body = request.form.get("reason")
    mail.send(msg)
    return render_template('home.html')

#NOTE need to add a connection between flask and html form following the week of 3/29/23

# create user signup page
@app.get('/signup')
def signup_page():
    return render_template('signup.html')

@app.post('/signup')
def signup_form():
    return redirect('/my_account')

@app.get('/items')
def list_all_items():
    all_items = item_repository_singleton.get_all_items()
    return render_template('', list_items_active=True, items=all_items)

@app.get('/items/<int:item_id>')
def get_single_item(item_id):
    single_item = item_repository_singleton.get_item_by_id(item_id)
    return render_template('', item=single_item)


@app.get('/items/new')
def create_item_form():
    return render_template('', create_item_active=True)


@app.post('/items')
def create_item():
    item_name = request.form.get('item_name')
    price = request.form.get('price', type = float)
    category = request.form.get('category')
    description = request.form.get('description')
    condition = request.form.get('condition')
    if item_name == '' or price < 0 or category == '' or description == '' or condition == '':
        abort(400)
    created_item = item_repository_singleton.create_item()
    return redirect(f'/item/{created_item.item_id}')


@app.get('/items/search')
def search_items_by_category():
    found_items = []
    q = request.args.get('q', '')
    if q != '':
        found_items = item_repository_singleton.search_items(q)
    return render_template('', search_active=True, item=found_items, search_query=q)