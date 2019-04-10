def test_login(client, auth):
    assert client.get('/').status_code == 200
    response = auth.login()
    assert b'test' in response.data
    response = auth.login('tea@stevenscollege.edu', 'q')
    assert response.headers['Location'] == 'http://localhost/'
    response = auth.login('teacher@stevenscollege.edu', 'qwerty')
    assert response.headers['Location'] == 'http://localhost/home'
