from app import app
def test_update_account(test_app):
    #Creates account, updates it then ensures data was changed
    response = test_app.post('/signup', data={

        'fname' : "bob",
        'lname' : "robert",
        'email' :"bob@gmail.com",
        'username' : "user56789",
        'user_pass' : "1123456789"
    }, follow_redirects=True)

    response = test_app.get('/my_account')
    assert response.status_code == 200
    
    response = test_app.post('/update_account', data={

        'email' :"newbob@gmail.com",
        'username' : "newuser56789",
        'user_pass' : "new1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "My Account" in data
    assert "Bob" in data
    assert "Robert" in data
    assert "newbob@gmail.com" in data
    assert "newuser56789" in data




    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200

    #Tries to update account with some bad information
    response = test_app.post('/signup', data={

        'fname' : "bob",
        'lname' : "robert",
        'email' :"bob@gmail.com",
        'username' : "user56789",
        'user_pass' : "1123456789"
    }, follow_redirects=True)

    response = test_app.get('/my_account')
    assert response.status_code == 200


    response = test_app.post('/update_account', data={
        'email' :"bob@gmail.com",
        'username' : "newuser56789",
        'user_pass' : "new1123456789"
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Please enter your new account credentials" in data

    
    response = test_app.post('/update_account', data={
        'email' :"newbob@gmail.com",
        'username' : "user56789",
        'user_pass' : "new1123456789",
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Please enter your new account credentials" in data


    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200





