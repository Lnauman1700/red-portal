def test_grades_validation(client, auth):
    with client:
        response = client.get('/assignments/1/grades')
        assert response.headers['Location'] == 'http://localhost/'
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/assignments/1/grades')
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401
    with client:
        auth.login()
        response = client.get('/assignments/1/grades')
        assert response.status_code == 200

def test_grades_page(client, auth):
    auth.login()
    # test that the page loads correctly
    response = client.get('/assignments/1/grades')
    assert b'<h1>Grades</h1>' in response.data

    # students who are in the session are listed
    response = client.get('/assignments/2/grades')
    assert b'student@stevenscollege.edu' in response.data
    assert b'<input type="number" name="2">' in response.data

    # make sure submission redirects you to the assignment Page
    response = client.post('/assignments/2/grades', data={
    2: 75
    })
    assert response.headers['Location'] == 'http://localhost/assignments/1/grades
    assert b'<input type="number" name="2" value="75">' in response.data
