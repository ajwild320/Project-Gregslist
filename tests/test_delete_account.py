from app import app
def test_delete_account(test_app):
    #Creates account, deletes it then ensures account was deleted by creating same account again
    response = test_app.post('/signup', data={

        'fname' : "bob",
        'lname' : "robert",
        'email' :"bob@gmail.com",
        'username' : "user56789",
        'user_pass' : "1123456789"
    }, follow_redirects=True)

    response = test_app.get('/my_account')
    assert response.status_code == 200

    response = test_app.post('/deactivate_account', data = {
        'answer' : 'Yes'
    }, follow_redirects = True)

    assert response.status_code == 200

    response = test_app.post('/signup', data={

        'fname' : "bob",
        'lname' : "robert",
        'email' :"bob@gmail.com",
        'username' : "user56789",
        'user_pass' : "1123456789"
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert "Bob" in data
    assert "Robert" in data
    assert "bob@gmail.com" in data
    assert "user56789" in data