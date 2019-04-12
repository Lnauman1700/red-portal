from flask import g, session

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form method="post">' in response.data

def test_login_logout(client, auth):
    assert client.get('/').status_code == 200

    # asserts that we go back to index if login fails
    with client:
        response = auth.login()
        assert response.headers['Location'] == 'http://localhost/'
        assert session['user_id'] == None
        assert g.user == None

    # assert that correct login works
    with client:
        response = auth.login('teacher@stevenscollege.edu', 'qwerty')
        assert response.headers['Location'] == 'http://localhost/home'
        assert session['user_id'] == 1
        client.get('/home')
        assert g.user[0] == 1

    # once logged in, check if logout works
    with client:
        response = auth.login('teacher@stevenscollege.edu', 'qwerty')
        response = client.get('/home')
        response = client.get('/logout')
        assert response.headers['Location'] == 'http://localhost/'
        assert session['user_id'] == None
        client.get('/')
        assert g.user == None
