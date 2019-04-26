def test_assignments_route(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments')
        assert 200 == response.status_code
        assert b'<h1>Assignments</h1>' in response.data
        assert b"<form method='POST'>" in response.data
        assert b'Delete Database' in response.data
        assert b'<option value="1">CSET 155 A</option>' in response.data        
        # TODO: add new function to test creating a assignment
        
def test_creating_assignment(client, auth):
    with client:
        auth.login()
        response = client.post('/assignments', data={
        'sess': 1,
        'assignment_name': '',
        'info': 'h',
        })
        assert b'<p>assignment name fields required</p>' in response.data
        assert 200 == response.status_code
        assert b"<form method='POST'>" in response.data
        response = client.post('/assignments', data={
        'sess': 1,
        'assignment_name': 'Test This statement',
        'info': 'h',
        })
        assert response.status_code == 302
        response = client.get('/assignments')
        assert b'Test This statement' in response.data

def test_assignments_auth(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments/98')
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401
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
            'assignment': 'Test This statement',
            'info': 'h',
            })
        assert response.status_code == 302
        response = client.get('/assignments')
        assert b'Test This statement' in response.data
