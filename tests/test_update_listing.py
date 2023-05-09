from app import app
from src.repositories.item_repository import item_repository_singleton
def test_update_listing(test_app):

 #Signs up, adds listing, checks to see if it exists
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

    item = item_repository_singleton.search_items_name("Gaming Mouse")
    response = test_app.post("/u")