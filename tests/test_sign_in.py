from app import app
def test_sign_in(test_app):   


    #Happy path: creates account, logs out, then tries to sign in, then logs out
    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    test_app.get('/log_out')

    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Bob" in data
    assert "Robert" in data
    assert "bob@gmail.com" in data
    assert "user56789" in data
    
    test_app.get('/log_out')
    #Tries to sign in while already signed in
    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200

    response = test_app.get('/sign_in', follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "My Account" in data
    assert "Bob" in data
    assert "Robert" in data
    assert "bob@gmail.com" in data
    assert "user56789" in data
    test_app.get('/log_out')

    #Tries to sign in with bad information
    response = test_app.post('/sign_in', data={
    'username' : "user5678",
    'user_pass' : "1123456789"
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Welcome back! Please sign in below." in data

    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "112345689"
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Welcome back! Please sign in below." in data

    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200

    #Tries to sign in while already signed in from sign up

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200

    response = test_app.get('/sign_in', follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "My Account" in data
    assert "Bob" in data
    assert "Robert" in data
    assert "bob@gmail.com" in data
    assert "user56789" in data

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200


