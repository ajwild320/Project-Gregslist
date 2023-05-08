from src.models import db, users
# from sqlalchemy import update
class UserRepository:

    def add_user(self, fname, lname, username, user_password, user_email):
        new_user = users(fname, lname, username, user_password, user_email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_username(self, username):
        my_user = users.query.filter_by(username=username).first() 
        return my_user
    
    def get_user_by_email(self, email):
        my_user = users.query.filter_by(user_email=email).first() 
        return my_user
    
    def get_user_by_username(self, username):
        my_user = users.query.get(username) 
        return my_user

    def change_email(self, email, old_user):
        users.query.filter_by(username=old_user).first().user_email = email
        print(email)
        db.session.commit()
    #change user's username
    def change_user(self,new_user, old_user):
        users.query.filter_by(username=old_user).first().username = new_user
        db.session.commit()

    def change_pass(self, input_pass, old_user):
        users.query.filter_by(username=old_user).first().user_password = input_pass
        db.session.commit()
    
    def delete_user(self, username):
        db.session.delete(users.query.filter_by(username=username).first())
        db.session.commit()
    

#for use in other files
user_repository_singleton = UserRepository() 