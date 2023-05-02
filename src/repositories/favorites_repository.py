from src.models import db, users, Item, favorites_list

class favoritesRepository:

    # insert a new favorite into the database
    def insert_favorite(self, username, item_id):
        new_favorite = favorites_list(username, item_id) # create a new favorite object
        db.session.add(new_favorite) # add the favorite to the session
        db.session.commit()
        return new_favorite

    # delete a favorite from the database
    def delete_favorite(self, username, item_id):
        favorite = favorites_list.query.filter_by(username=username, item_id=item_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return True
    
    
    # get all favorites from the database by username
    def get_all_favorites(self, username):
        all_favorites = favorites_list.query.filter_by(username=username).all()
        return all_favorites


#for use in other files
favorites_repository_singleton = favoritesRepository() 