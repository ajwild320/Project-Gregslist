from flask import Flask, render_template, request, redirect, abort, session, url_for
from datetime import datetime
from flask_mail import Mail, Message
from src.models import db, Item, users, favorites_list, comments
from src.repositories.item_repository import item_repository_singleton
from dotenv import load_dotenv
from src.repositories.user_repository import user_repository_singleton
from src.repositories.favorites_repository import favorites_repository_singleton
from src.repositories.comments_repository import comments_repository_singleton
from security import bcrypt
import os
load_dotenv()

app = Flask(__name__,static_folder='my_static_folder')

#DB connection and setup
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI']\
      =  f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)
bcrypt.init_app(app)

#Mail connection and setup
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

@app.get('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.post('/contact_us')
def contact_us_email():
    name = request.form.get("name")
    email = request.form.get("email")
    reason = request.form.get("reason")
    if name.strip() == '' or email.strip() == '' or reason.strip() == '':
        return redirect('/contact_us')
    else:
        subject_line = "{} is reaching out".format(name)
        body = "{} is reaching out. They can be responded to at {}. They are reaching out in regards of: '{}'".format(name, email, reason)
        msg = Message(subject_line, sender = 'gregslist.customer.service@gmail.com', recipients = ['gregslist.customer.service@gmail.com', email])
        msg.body = body
        mail.send(msg)
        return render_template('home.html')

@app.get('/my_account')
def my_account():
    try:
        user = session['user']
        hour = datetime.now().hour
        if hour > 4 and hour < 11:
            time_of_day = "Morning"
        elif hour >= 11 and hour < 17:
            time_of_day = "Afternoon"
        else:
            time_of_day = "Evening"
        return render_template('my_account.html', user=user, time_of_day=time_of_day)
    except:
        return render_template('sign_in.html')

@app.get('/sign_in')
def to_sign_in_page():
    if 'user' not in session:
        return render_template('sign_in.html')
    return redirect("/my_account")

@app.post('/sign_in')
def sign_in():
    sign_in_user = str(request.form.get('username'))
    sign_in_pass = str(request.form.get('user_pass'))

    existing_user = users.query.filter_by(username = sign_in_user).first()

    if not existing_user:
        return redirect("/sign_in")
    
    if not(bcrypt.check_password_hash(existing_user.user_password, sign_in_pass )):
        return redirect("/sign_in")

    session['user'] = {
        'first_name' : users.query.filter_by(username = sign_in_user).first().first_name,
        'last_name' : users.query.filter_by(username = sign_in_user).first().last_name,
        'username': sign_in_user,
        'email' : users.query.filter_by(username = sign_in_user).first().user_email
    }

    return redirect('/my_account')

@app.get("/log_out")
def logout():
     try:
        del session['user']
        return redirect("/")
     except:
        return redirect('/')

@app.get('/deactivate_account')
def deactivate_account():
    try:
        user = session['user']
        return render_template('deactivate_account.html', user=user)
    except:
        return render_template('sign_in.html')

@app.post('/deactivate_account')
def deactivate():
    answer = str(request.form.get('answer'))
    if answer == 'Yes':
        user = session['user']
        print("HERE")
        username = user.get('username')
        user_repository_singleton.delete_user(username)
        del session['user']
        return redirect("/signup")
    
    else:
        return redirect('/my_account')

@app.get('/report_post/<int:item_id>')
def report_post(item_id):    
    try:
        user = session['user']
        single_item = item_repository_singleton.get_item_by_id(item_id)
        return render_template('report_post.html', item=single_item)
    except:
        return render_template('sign_in.html')

@app.post('/report_post/<int:item_id>')
def report_post_email(item_id):
    try:
        user = session['user']
        id = item_id
        reporter_fname = user.get('first_name')
        reporter_lname = user.get('last_name')
        reporter_email = user.get('email')
        reason = request.form.get("reason")
        if reason.strip() == '':
            return redirect('/report_post/{}'.format(item_id))
        msg = Message('Report Post', sender = 'gregslist.customer.service@gmail.com', recipients = ['gregslist.customer.service@gmail.com', reporter_email])
        msg.body = "{} {} is reaching out. They can be contacted back at {} if further details are needed. They are reporting post #{} for the reason(s) of: ' {}'".format(reporter_fname, reporter_lname, reporter_email, id, reason)
        mail.send(msg)
        return render_template('home.html')
    except:
        return redirect('/report_post/{}'.format(item_id))

@app.get('/items/<int:item_id>')
def get_single_item(item_id):
    single_item = item_repository_singleton.get_item_by_id(item_id)
    return render_template('single_item.html', item=single_item)

@app.post('/items')
def create_item():
    user = session['user']
    seller = user.get('username')
    item_name = request.form.get('item_name').title()
    price = request.form.get('price', type = float)
    category = request.form.get('category')
    description = request.form.get('description')
    condition = request.form.get('condition')
    if item_name.strip() == '' or price == 0 or price == None or price < 0 or category == None or description.strip() == '' or condition == None:
        return redirect('/create_listing')
    created_item = item_repository_singleton.create_item(item_name, price, category, description, condition, seller)
    return redirect(f'/items/{created_item.item_id}')

@app.get('/items/my_items/<username>')
def my_items(username):
    user = session['user']
    username = user.get('username')
    if(username != user["username"]):
        return redirect("/my_account")
    user_item = item_repository_singleton.get_all_items()
    return render_template('my_listings.html', item=user_item, username=username)

@app.get('/items/delete/<int:item_id>')
def delete_item_form(item_id):
    try:
        user = session['user']
        curr_item = item_repository_singleton.get_item_by_id(item_id)
        if(curr_item.username != user["username"]):
            return redirect("/my_account")
        user_item = item_repository_singleton.get_item_by_id(item_id)
        return render_template('delete_item.html', user=user, item=user_item)
    except:
        return render_template('sign_in.html')

@app.post('/items/delete/<int:item_id>')
def delete_item(item_id):
    answer = str(request.form.get('answer'))
    if answer == 'Yes':
        item_repository_singleton.delete_item(item_id)
        return redirect('/my_account')
    elif answer == 'No':
        return redirect('/my_account')
    
@app.get('/items/update/<int:item_id>')
def update_item_form(item_id):
    user = session['user']

    curr_item = item_repository_singleton.get_item_by_id(item_id)
    if(curr_item.username != user["username"]):
        return redirect("/my_account")
    user_item = item_repository_singleton.get_item_by_id(item_id)
    return render_template('update_item.html', user=user, item=user_item)

@app.post('/items/update/<int:item_id>')
def update_item(item_id):
        user = session['user']
        existing_item = item_repository_singleton.get_item_by_id(item_id)

        seller = user.get('username')
        new_item_name = request.form.get('item_name').title()
        new_price = request.form.get('price', type = float)
        new_category = request.form.get('category')
        new_description = request.form.get('description')
        new_condition = request.form.get('condition')
        
        if new_item_name.strip() == '':
            existing_item.item_name = existing_item.item_name
        else:
            existing_item.item_name = new_item_name

        if new_price == None:
            existing_item.price = existing_item.price
        else:
            existing_item.price = new_price
        
        if new_category == None:
            existing_item.category = existing_item.category
        else:
            existing_item.category = new_category

        if new_description.strip() == '':
            existing_item.description = existing_item.description
        else:
            existing_item.description = new_description

        if new_condition == None:
            existing_item.condition = existing_item.condition
        else:
            existing_item.condition = new_condition

        existing_item.username = seller
        db.session.commit()
        return redirect('/my_account')

@app.get('/item/interested/<int:item_id>')
def interested_form(item_id):
    user = session['user']
    interested_item = item_repository_singleton.get_item_by_id(item_id)
    return render_template('interested.html' ,user=user, item=interested_item)

@app.post('/item/interested/<int:item_id>')
def interested(item_id):
    try:
        user = session['user']
        interested_fname = user.get('first_name')
        interested_lname = user.get('last_name')
        interested_email = user.get('email')

        interested_item = item_repository_singleton.get_item_by_id(item_id)
        seller = interested_item.username
        interested_name = interested_item.item_name

        seller_user = user_repository_singleton.get_user_by_username(seller)
        seller_email = seller_user.user_email

        info = request.form.get("info")
        form_message = request.form.get("message")

        if info == None and form_message.strip() == "":
            return redirect('/item/interested/{}'.format(item_id))

        msg = Message('Interested about your listing!', sender = 'gregslist.customer.service@gmail.com', recipients = ['gregslist.customer.service@gmail.com', interested_email, seller_email])
        msg.body = "{} {} is reaching out. They can be contacted back at {}. They are reaching out about you product named '{}' for additional information on '{}' and in regards of '{}'".format(interested_fname, interested_lname, interested_email, interested_name, info, form_message)
        mail.send(msg)
        return redirect('/my_account')
    except:
        abort(400)

@app.get('/listings')
def display_all_listings():
    if 'user' in session:
        user = session['user']
        # name = request.args.get('name', '')
        # if name != '':
            # found_items = item_repository_singleton.search_items_name(name)
        return render_template('listings.html')
    else:
        return render_template('sign_in.html')

@app.get('/listings/<id>')
def get_category(id):
    print(id)
    if 'user' in session:
        cat_name = id
        found_items_cat = []
        found_items_cat = item_repository_singleton.search_items_category(cat_name)
        return render_template('listings.html', search_active=True,items=found_items_cat)
    else:
        return render_template('sign_in.html')

@app.get('/items/search')
def search_items_by_name():
    try:
        user = session['user']
        found_items = []
        name = request.args.get('name', '')
        if name != '':
            found_items = item_repository_singleton.search_items_name(name)
        return render_template('search.html', search_active=True, item=found_items, search_query=name)
    except:
        return render_template('sign_in.html')
    
# create user signup page
@app.get('/signup')
def signup_page():
    if 'user' not in session:
        return render_template('signup.html')
    return redirect("/my_account")

@app.post('/signup')
def signup_form():    
    new_fname = str(request.form.get('fname').title())
    new_lname = str(request.form.get('lname').title())
    new_email = str(request.form.get('email'))
    new_user = str(request.form.get('username'))
    new_pass = str(request.form.get('user_pass'))

    if not new_fname or not new_lname or not new_email or not new_user or not new_pass\
            or new_fname.strip() == '' or new_lname.strip() == '' or new_email.strip() == '' or new_user.strip() == '' or new_pass.strip() == ''\
            or '@' not in new_email or '.' not in new_email:
        return redirect("/signup")

    new_pass = bcrypt.generate_password_hash(new_pass).decode()
    print("HERE")
    #checks to make sure user does not already exist.
    existing_user = users.query.filter_by(username = new_user).first()
    if existing_user:
        return redirect("/signup")
    existing_user = users.query.filter_by(user_email = new_email).first()
    if existing_user:
        return redirect("/signup")
    
    user_repository_singleton.add_user(new_fname, new_lname, new_user, new_pass, new_email)

    session['user'] = {
        'first_name' : new_fname,
        'last_name' : new_lname,
        'username': new_user,
        'email' : new_email
    }
    return redirect('/my_account')

@app.get('/update_account')
def update_page():
    try:
        user = session['user']
        if user:
            return render_template('update_account.html')
    except:
        return render_template('sign_in.html')

@app.post('/update_account')
def update_form():
    user = session['user']

    old_user = user["username"]
    new_user = str(request.form.get('username'))
    new_email = str(request.form.get('email'))
    new_pass = str(request.form.get('password'))
    print("NEW PASS " + new_pass)
    if new_user == None or new_pass == None or user_repository_singleton.get_user_by_email(new_email) != None or user_repository_singleton.get_user_by_username(new_user) != None or new_pass == None:
        return redirect("/update_account")
    data = {
        'first_name' : user['first_name'],
        'last_name' : user['last_name'],
        'username': new_user,
        'email' : new_email
    }
    

    new_pass = bcrypt.generate_password_hash(new_pass).decode()
    user_repository_singleton.change_email(new_email, old_user)
    user_repository_singleton.change_pass(new_pass, old_user)
    user_repository_singleton.change_user(new_user, old_user)

    session['user'] = data
    user = session['user']
    return redirect('/my_account')

@app.get('/create_listing')
def user_create_listing_page():
    try:
        user = session['user']
        return render_template('create_listing.html')
    except:
        return render_template('sign_in.html')    

# show favorites list page
@app.get('/favorites_list_fav')    
def fav_list():
    user = session['user']
    username = user.get('username')
    favorites = favorites_repository_singleton.get_all_favorites(username)  # get the list of favorites for the current user
    return render_template('favorites_list_fav.html', favorites=favorites)
    
# add favorite to favorites list based on user session and item id of currently selected item
@app.post('/favorites_list_fav/<int:item_id>')
def fav_list_add_fav(item_id):
    user = session['user']
    username = user.get('username')
    favorites = favorites_repository_singleton.get_all_favorites(username)

    # uses for loop to check if item is already in favorites list, if it is then
    # it is not added to favorites list and the redirect returns the user to the
    # listing page they were on when they tried to add the item to favorites again.
    for favorite in favorites:
        if item_id == favorite.item_id:
            return redirect(request.referrer)

    single_item =item_repository_singleton.get_item_by_id(item_id)
    favorites_repository_singleton.insert_favorite(username, single_item.item_id)

    return redirect(url_for('fav_list'))

# remove favorite from favorites list based on user session and item id of selected item
@app.post('/favorites_list_fav/delete/<int:item_id>')
def fav_list_delete_fav(item_id):
    user = session['user']
    username = user.get('username')
    single_item =item_repository_singleton.get_item_by_id(item_id)
    favorites_repository_singleton.delete_favorite(username, single_item.item_id)

    return redirect(url_for('fav_list'))

# get all comments for a single item
# possible change: /items/<int:item_id> <-------> old: /single_item/<int:item_id>
@app.get('/single_item/<int:item_id>')
def get_all_comments(item_id):
    single_item = item_repository_singleton.get_item_by_id(item_id)
    comments = comments_repository_singleton.get_all_comments_by_item_id(single_item.item_id)

    return render_template('single_item.html', item=single_item, comments=comments)

# user adds comment to a single item's comments list
@app.post('/single_item/<int:item_id>')
def add_comment(item_id):
    user = session['user']
    username = user.get('username')
    single_item = item_repository_singleton.get_item_by_id(item_id)
    comment = request.form.get('comment')

    if comment == '' or comment == None:
        return redirect(request.referrer)
    
    comments_repository_singleton.insert_comment(username, single_item.item_id, comment)
    return redirect(url_for('get_all_comments', item_id=item_id))

# delete a single comment from a single item's comments list
@app.post('/single_item/delete/<int:comment_id>')
def remove_comment(comment_id):
    comment_id = request.form.get('comment_id')
    
    comments_repository_singleton.delete_comment(comment_id)
    return redirect(request.referrer)

# update a single comment from the comments list of any given item
@app.post('/single_item/update/<int:comment_id>')
def update_comment(comment_id):
    comment = request.form.get('new_comment')
    comment_id = request.form.get('comment_id')

    comments_repository_singleton.update_comment(comment_id, comment)
    return redirect(request.referrer)