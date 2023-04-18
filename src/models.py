from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key = True)
    item_name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    condition = db.Column(db.String(255), nullable = False)

    def __init__(self, item_name: str, price: float, category: str, description: str, condition: str) -> None:
        self.item_name = item_name
        self.price = price
        self.category = category
        self.description = description
        self. condition = condition

    def __repr__(self) -> str:
        return f'Item(item_name = {self.item_name}, price = {self.price}, category = {self.category}, description = {self.description}, condition = {self.condition})'

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
