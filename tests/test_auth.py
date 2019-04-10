def test_login(client, auth):
    # on index, we get a 200 status code
    assert client.get('/').status_code == 200
    # w/ wrong info, we redirect to index page
    response = auth.login('tea@stevenscollege.edu', 'q')
    assert response.headers['Location'] == 'http://localhost/'
    # w/ correct info, we log in and redirect to home.
    response = auth.login('teacher@stevenscollege.edu', 'qwerty')
    assert response.headers['Location'] == 'http://localhost/home'
