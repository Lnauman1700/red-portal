from flask import g, session

def test_validation(client, auth):

    with client:
        response = client.get('/sessions')
        assert response.headers['Location'] == 'http://localhost/'
        response = client.get('/sessions/1')
        assert response.headers['Location'] == 'http://localhost/'
        response = client.get('/sessions/create')
        assert response.headers['Location'] == 'http://localhost/'
    # make sure user who accesses route is a teacher
    with client:
        auth.login()
        response = client.get('/sessions')
        assert b'<ul>' in response.data
        assert b'CSET 155A' in response.data
    #if student accesses page, then bounce them back to home.
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/sessions')
        assert b'You are not permitted to view this page' in response.data
        # if student tries accessing sessions/1, then they aren't permitted to view page
        response = client.get('/sessions/1')
        assert b'You are not permitted to view this page' in response.data
        # if student tries accessing sessions/create, not permitted to view page
        response = client.get('/sessions/create')
        assert b'You are not permitted to view this page' in response.data
    with client:
        # if teacher tries viewing sessions which doesn't belong to them, not permitted to view page
        auth.login('teacher2@stevenscollege.edu', 'h')
        response = client.get('/sessions')
        assert b'CSET 155A' not in response.data


def test_session_route(client, auth):

    auth.login()
    assert client.get('/sessions').status_code == 200

    with client:
        response = client.get('/sessions/1')
        # represents the page which loaded, nice if result it's dynamic
        assert b'<p>CSET 155A</p>' in response.data
        assert b'<p>2:00 - 4:20 MF</p>' in response.data

        # putting in new data displays a success, also shows that data in the page
        response = client.post('/sessions/1', data=dict(
            session_letter='B',
            session_time='4:00 - 6:00 MWF',
            student='student@stevenscollege.edu',
        ))
        assert b'Session successfully updated' in response.data
        assert b'CSET 155B' in response.data
        assert b'4:00 - 6:00 MWF' in response.data

        # if you put in student who doesn't exist, give error message and don't replace anything
        response = client.post('/sessions/1', data=dict(
            session_letter='P',
            session_time='This time wont show up',
            student='not@student',
        ))
        assert b'A student with the email not@student does not exist' in response.data
        assert b'CSET 155B' in response.data
        assert b'4:00 - 6:00 MWF' in response.data

        #if you add in one or more blank students, the code still runs
        response = client.post('/sessions/1', data=dict(
            session_letter='P',
            session_time='This time will show up',
            student='',
        ))
        assert b'Session successfully updated' in response.data
        assert b'CSET 155P' in response.data
        assert b'This time will show up' in response.data

    with client:
        response = client.get('/sessions/79')
        assert response.status_code == 404
        assert b'Session does not exist' in response.data


def test_session_create(client, auth):
    #page shows up when teacher is logged in
    auth.login()
    assert client.get('/sessions/create').status_code == 200
    #form shows up when route is acessed
    response = client.get('/sessions/create')
    assert b'<label>Session Letter:' in response.data

    # adding in a new session with blank student fields should work
    response = client.post('/sessions/create', data=dict(
        course_id=1,
        session_letter='C',
        session_time='2:00 - 2:40 MWF',
        student='',
    ))
    assert b'Session successfully created' in response.data
    response = client.get('/sessions')
    assert b'CSET 155C' in response.data

    # adding in a new session with students who exist should work
    response = client.post('/sessions/create', data=dict(
        course_id=1,
        session_letter='O',
        session_time='2:00 - 2:40 MWF',
        student='student@stevenscollege.edu',
    ))
    assert b'Session successfully created' in response.data
    response = client.get('/sessions')
    assert b'CSET 155O' in response.data

    # making a new session with students who don't exist shouldn't work
    response = client.post('/sessions/create', data=dict(
        course_id=1,
        session_letter='H',
        session_time='2:00 - 2:40 MWF',
        student='not@student',
    ))
    assert b'A student with the email not@student does not exist' in response.data
