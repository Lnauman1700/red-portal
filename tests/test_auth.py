from flask import g, session

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form method="post">' in response.data

def test_login(client, auth):
    # on index, we get a 200 status code
    assert client.get('/').status_code == 200

    # w/ wrong info, we redirect to index page
    assert session['user_id'] == None
    response = auth.login('tea@stevenscollege.edu', 'q')
    assert response.headers['Location'] == 'http://localhost/'
    assert session['user_id'] == None

    # login happens and user session is stored
    response = auth.login('teacher@stevenscollege.edu', 'qwerty')
    assert response.headers['Location'] == 'http://localhost/home'
    assert session['user_id'] == 1
    assert g.user[1] == 'teacher@stevenscollege.edu'

    response = auth.logout()
    assert response.headers['Location'] == 'http://localhost/'
    assert session['user_id'] == None
    assert g.user == None
