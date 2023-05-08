from app import app
def test_create_listing(test_app):

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

    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Gaming Mouse" in data
    assert "$10.20" in data
    assert "a description" in data
    assert "user56789" in data
    assert "Excellent" in data
    response = test_app.get('/listings/toys')
    assert response.status_code == 200

    data = response.data.decode('utf-8')
    assert "Gaming Mouse" in data
    assert "$10.20" in data
    # assert "a description" in data
    assert "Excellent" in data


    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200

    response = test_app.get("/create_listing", follow_redirects = True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Welcome back! Please sign in below." in data
