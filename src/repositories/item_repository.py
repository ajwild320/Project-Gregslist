from src.models import Item, db

class ItemRepository:
    
    #Gets all the items from the DB
    def get_all_items(self):
        all_items = Item.query.all()
        return all_items

    #Gets an item from the DB using the item's ID number
    def get_item_by_id(self, item_id):
        one_item = Item.query.get(item_id)
        return one_item

    #Creates a new item in the DB
    def create_item(self, item_name, price, category, description, condition):
        new_item = Item(item_name, price, category, description, condition)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    #Gets all items matching a variety of substrings
    def search_items(self, item_name):
        item = Item.query.filter(Item.item_name.ilike(item_name)).all()
        return item


# Singleton to be used in other modules
item_repository_singleton = ItemRepository()