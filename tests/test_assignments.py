from flask import request
def test_assignments_route(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments')
        assert 200 == response.status_code
        assert b'<h1>Assignments</h1>' in response.data
        assert b"<form method='POST'>" in response.data
        assert b'Delete Database' in response.data
        assert b'<option value="1">CSET 155 A</option>' in response.data
        # let's actually update that shit, submit a post request w/ data that will work
        response = client.post('/assignments/1', data={
            'assignment': '',
            'info': 'h',
        })
        assert response.status_code == 200
        assert b'<p>assignment name fields required</p>' in response.data
        response = client.post('/assignments/1', data={
            'session': '',
            'assignment': 'I'
        })
        # assert b'assignment name fields required' in response.data
        response = client.post('/assignments/1', data={
            'assignment': 'h',
            'info': 'h',
        })
        assert response.status_code == 302
        assert b'h' in response.data

def test_assignments_auth(client, auth):
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/assignments')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401
        response = client.get('/assignments/1')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401

def test_course_update(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments/1')
        assert response.status_code == 200
        assert b"<form method='POST'>" in response.data

        response = client.post('/assignments/1', data={
            'assignment': '',
            'info': 'h',
        })
        assert b'<p>assignment name fields required</p>' in response.data
        assert 200 == response.status_code

        assert b"<form method='POST'>" in response.data

        response = client.post('/assignments/1', data={
            'session': '',
            'assignment': 'I',
        })
        assert b'<p>assignment name fields required</p>' in response.data
        assert 200 == response.status_code

        response = client.post('/assignments/1', data={
            'assignment': 's',
            'info': 'h',
            })
        assert response.status_code == 302
        assert b's' in response.data
