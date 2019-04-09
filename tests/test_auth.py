def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login('teacher@stevenscollege.edu', 'qwerty')
    assert response.headers['Location'] == 'http://localhost/'
