
from app import app
def test_sign_up(test_app):
    #Testing path where user enters their sign in info, then deletes account. Ensures happy path functionality of creating account.
    response = test_app.post('/signup', data={

        'fname' : "bob",
        'lname' : "robert",
        'email' :"bob@gmail.com",
        'username' : "user56789",
        'user_pass' : "1123456789"
    }, follow_redirects=True)

    response = test_app.get('/my_account')
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Bob" in data
    assert "Robert" in data
    assert "bob@gmail.com" in data
    assert "user56789" in data

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200
    


    #Makes account, then tries to go back to signup page, then logs out. Then tries to sign up with existing info
    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200

    response = test_app.get('/signup', follow_redirects = True)
    data = response.data.decode('utf-8')
    assert "My Account" in data

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200


    test_app.get('/log_out')

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200
    #The next five responses are attempts to send bad data through the sign up page and ensuring a redirect back to sign up page
    response = test_app.post('/signup', data={

    'fname' : "",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Sign up for your free account today!" in data

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Sign up for your free account today!" in data

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"",
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Sign up for your free account today!" in data

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Sign up for your free account today!" in data

    response = test_app.post('/signup', data={

    'fname' : "bob",
    'lname' : "robert",
    'email' :"bob@gmail.com",
    'username' : "user56789",
    'user_pass' : ""
    }, follow_redirects=True)

    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "Sign up for your free account today!" in data





    response = test_app.post('/sign_in', data={
    'username' : "user56789",
    'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200
