from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    condition = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), foreign_key = True)

    def __init__(self, item_name: str, price: float, category: str, description: str, condition: str, username: str) -> None:
        self.item_name = item_name
        self.price = price
        self.category = category
        self.description = description
        self.condition = condition
        self.username = username

    def __repr__(self) -> str:
        return f'Item(item_name = {self.item_name}, price = {self.price}, category = {self.category}, description = {self.description}, condition = {self.condition}, username = {self.username})'

class users(db.Model):
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), primary_key=True)
    user_password = db.Column(db.String(255))
    user_email = db.Column(db.String(255))

    def __init__(self, fname, lname, username, user_password, user_email) -> None:
        self.first_name = fname
        self.last_name = lname
        self.username = username
        self.user_password = user_password
        self.user_email = user_email
    
    def __repr__(self) -> str:
        return f'users(first_name = {self.first_name}, last_name = {self.last_name}, username = {self.username}, user_password = {self.user_password}, user_email = {self.user_email})'

class favorites_list(db.Model):
    username = db.Column(db.String(255), nullable = False, foreign_key = True, primary_key = True)
    item_id = db.Column(db.Integer, nullable = False, foreign_key = True, primary_key = True)

    def __init__(self, username, item_id) -> None:
        self.username = username
        self.item_id = item_id
    
    def __repr__(self) -> str:
        return f'favorites_list(username = {self.username}, item_id = {self.item_id})'
    
class comments(db.Model):
    username = db.Column(db.String(255), nullable = False, foreign_key = True)
    item_id = db.Column(db.Integer, nullable = False, foreign_key = True)
    comment = db.Column(db.String(500), nullable = False)
    comment_id = db.Column(db.Integer, nullable = False, autoincrement=True, primary_key = True)

    def __init__(self, username, item_id, comment) -> None:
        self.username = username
        self.item_id = item_id
        self.comment = comment

    def __repr__(self) -> str:
        return f'comments(username = {self.username}, item_id = {self.item_id}, comment = {self.comment}, comment_id = {self.comment_id})'