from src.models import db, users, Item, comments

class commentsRepository:

    def insert_comment(self, username, item_id, comment):
        new_comment = comments(username=username, item_id=item_id, comment=comment)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    
    def delete_comment(self, comment_id):
        db.session.delete(comments.query.get(comment_id))
        db.session.commit()
        return True
    
    def update_comment(self, comment_id, new_comment):
        comment = comments.query.get(comment_id)
        comment.comment = new_comment
        db.session.commit()
        return True
    
    def get_all_comments_by_item_id(self, item_id):
        all_comments = comments.query.filter_by(item_id=item_id).all()
        return all_comments
    
    def get_comment_by_id(self, comment_id):
        comment = comments.query.filter_by(comment_id=comment_id).first()
        return comment
    
#for use in other files
comments_repository_singleton = commentsRepository()