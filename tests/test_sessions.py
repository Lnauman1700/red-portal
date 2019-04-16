from flask import g, session

def test_validation(client, auth):
    # make sure user who accesses route is a teacher
    with client:
        auth.login()
        response = client.get('/sessions')
        assert b'<ul>' in response.data
    #if student accesses page, then bounce them back to home.
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/sessions')
        assert response.headers['Location'] == 'http://localhost/home'

def test_session_route(client, auth):

    assert client.get('/sessions').status_code == 200

    auth.login()
    with client:
        response = client.get('/sessions/1')
        # represents the page which loaded, nice if result it's dynamic
        assert b'<p>A</p>' in response.data
        assert b'<p>2:00 - 4:20 MF</p>' in response.data

        # if you put in existing student, give success message and bounce back to session page
        response = client.post('/sessions/1', data=dict(
            student=2
        ))
        assert b'<p>Student successfully added</p>' in response.data

        # if you put in student who doesn't exist, bounce back to page and give error message
        response = client.post('/sessions/1', data=dict(
            student=10000
        ))
        assert b'<p>Error adding student</p>'

    with client:
        assert client.get('/sessions/79').status_code == 404
