from src.models import db, users
# from sqlalchemy import update
class UserRepository:
    
    #ensures user has entered correct credentials
    def check_info(self, user_id, old_user, old_pass):
        return users.query.get(user_id).username == old_user and users.query.get(user_id).user_password == old_pass 


    def add_user(self, fname, lname, username, user_password, user_email):
        new_user = users(fname, lname, username, user_password, user_email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_id(self, user_id):
        my_user = users.query.get(user_id) 
        return my_user
    
    def get_user_by_username(self, username):
        my_user = users.query.get(username) 
        return my_user

    def change_email(self, user_id, email, old_user, old_pass):
        if self.check_info(user_id, old_user, old_pass):
            users.query.get(user_id).user_email = email
            print(email)
            db.session.commit()
    #change user's username
    def change_user(self, user_id, new_user, old_user, old_pass):
        if self.check_info(user_id, old_user, old_pass) and self.validate_user(new_user):
            users.query.get(user_id).username = new_user
            db.session.commit()

    def change_pass(self, user_id, input_pass, old_user, old_pass):
        if self.check_info(user_id, old_user, old_pass):
            users.query.get(user_id).user_password = input_pass
            db.session.commit()

    #Checks if user signing up is repeat, by checking text file.
    def validate_user(self, test_username):
        if(users.query.filter_by(username = test_username ).first() == None):
            print("NEW USER IS HERE")
            return False
        return True
    
    def delete_user(self, user_id):
        db.session.delete(users.query.get(user_id))
        db.session.commit()
    

#for use in other files
user_repository_singleton = UserRepository() 