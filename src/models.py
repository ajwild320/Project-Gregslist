from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    user_password = db.Column(db.String(255))
    user_email = db.Column(db.String(255))

    def __init__(self, fname, lname, username, user_password, user_email) -> None:
        self.first_name = fname
        self.last_name = lname
        self.username = username
        self.user_password = user_password
        self.user_email = user_email
