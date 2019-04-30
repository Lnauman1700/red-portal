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
    assert b'<h1>CSET 155A - Delete Database Grades</h1>' in response.data

    # students who are in the session are listed
    response = client.get('/assignments/2/grades')
    assert b'student@stevenscollege.edu' in response.data

    # log a grade for student id 2
    response = client.post('/assignments/2/grades', data={
        2: 900,
        5: ''
    })

    # students who have grades logged already have their grade show up
    assert b'<input type="number" name="2" value="900">' in response.data

    # students without grades logged already have None values
    assert b'<input type="number" name="5" value="None">' in response.data

    # make sure we can update grades
    response = client.post('/assignments/2/grades', data={
        2: 85,
        5: 75
    })
    assert b'<input type="number" name="2" value="85">' in response.data
    assert b'<input type="number" name="5" value="75">' in response.data
