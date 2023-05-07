from app import app
def test_sign_out(test_app):

    #Create account, then log out, then sign in
    test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    response = test_app.get('/log_out')

    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200    

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200
    #Tries to log out while not signed in
    response = test_app.get("/log_out", follow_redirects = True)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Our Products" in data
    

