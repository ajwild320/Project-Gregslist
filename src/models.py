from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    category = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    condtion = db.Column(db.String(255), nullable = False)

    def __init__(self, item_name: str, price: float, category: str, description: str, condition: str) -> None:
        self.item_name = item_name
        self.price = price
        self.category = category
        self.description = description
        self. condtion = condition

    def __repr__(self) -> str:
        return f'Item(item_name = {self.item_name}, price = {self.price}, category = {self.category}, description = {self.description}, condition = {self.condtion})'