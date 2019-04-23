# wanna see that certain roles that access the page get let in sent out
def test_validation_my_courses(client, auth):
    with client:
        response = client.get('/my_courses')
        assert response.headers['Location'] == 'http://localhost/'
    with client:
        auth.login()
        response = client.get('/my_courses')
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        response = client.get('/my_courses')
        assert b"<table>"
        assert 200 == response.status_code
        assert b'<h1>My Courses</h1>' in response.data


# when a certain student logs in, their data should be shown.
def test_my_courses(client, auth):
    auth.login('student@stevenscollege.edu','asdfgh')
    response = client.get('/my_courses')
    assert b'Database CSET 155B' in response.data
    assert b'teacher@stevenscollege.edu' in response.data
    assert b'3:00-3:30 MTWHF' in response.data
    assert b'Water WET 000A' in response.data
    assert b'teacher2@stevenscollege.edu' in response.data
    assert b'6:00-8:00 MWF' in response.data
