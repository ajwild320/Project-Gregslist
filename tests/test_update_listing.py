from app import app
from src.repositories.item_repository import item_repository_singleton

def test_update_listing(test_app):
    with app.app_context():

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

        item = item_repository_singleton.search_items_name("Gaming Mouse")[0]
        response = test_app.post(f"/items/update/{item.item_id}",data={
            'item_name' : "Gaming Mouse 1",
            'price' : "10.3",
            'description' :"the description",
            'category' : "Misc",
            'condition' : "Good"
        }, follow_redirects=True)

        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert "My Account" in data

        response = test_app.get(f"/items/{item.item_id}")
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert "Gaming Mouse 1" in data
        assert "$10.30" in data
        assert "the description" in data
        assert "user56789" in data
        assert "Good" in data

        response = test_app.get('/log_out')
        response = test_app.post('/signup', data={

            'fname' : "john",
            'lname' : "doe",
            'email' :"john@gmail.com",
            'username' : "john1234",
            'user_pass' : "abcd"
        }, follow_redirects=True)

        #making sure other users cant access other's posts directly
        response = test_app.get(f"/items/update/{item.item_id}", follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert "My Account" in data

        response = test_app.post('/deactivate_account', data = {
            'answer' : 'Yes'
        }, follow_redirects = True)

        response = test_app.post('/sign_in', data={
            'username' : "user56789",
            'user_pass' : "1123456789"
        }, follow_redirects=True)
        assert response.status_code == 200

        response = test_app.post(f"/items/delete/{item.item_id}", data = {
            'answer' : 'Yes'
        }, follow_redirects = True)
        assert response.status_code == 200

        response = test_app.post('/deactivate_account', data = {
            'answer' : 'Yes'
        }, follow_redirects = True)

        assert response.status_code == 200