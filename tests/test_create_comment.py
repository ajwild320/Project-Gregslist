from app import app
from src.repositories.item_repository import item_repository_singleton
def test_update_listing(test_app):
    with app.app_context():

    #Signs up, adds listing, adds comment, checks if comment exists
        response = test_app.post('/signup', data={

            'fname' : "bob",
            'lname' : "robert",
            'email' :"bob@gmail.com",
            'username' : "user56789",
            'user_pass' : "1123456789"
        }, follow_redirects=True)

        response = test_app.get('/my_account')
        assert response.status_code == 200
        response = test_app.post('/items', data={

            'item_name' : "Gaming Mouse",
            'price' : "10.2",
            'description' :"a description",
            'category' : "Toys",
            'condition' : "Excellent"
        }, follow_redirects=True)

        item = item_repository_singleton.search_items_name("Gaming Mouse")[0]


        response = test_app.post(f"/items/{item.item_id}",data={

            'comment' : "Here is a new comment!"
             }, follow_redirects = True )
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert "Here is a new comment!" in data

        response = test_app.post(f"/items/delete/{item.item_id}", data = {
            'answer' : 'Yes'
        }, follow_redirects = True)
        assert response.status_code == 200

        response = test_app.post('/deactivate_account', data = {
            'answer' : 'Yes'
        }, follow_redirects = True)

        assert response.status_code == 200