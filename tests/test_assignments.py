from flask import request
def test_assignments_route(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments')
        assert 200 == response.status_code
        assert b'<h1>Assignments</h1>' in response.data
        assert b"<form method='POST'>" in response.data
        assert b'Delete Database' in response.data
        # let's actually update that shit, submit a post request w/ data that will work
        response = client.post('/assignment/1', data={
            'assignment': 'h',
            'info': 'h',
        })
        assert b'<li><a href="/assignments/1">h</a></li>' in response.data


def test_assignments_auth(client, auth):
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/assignments')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data

def test_course_update(client, auth):
    auth.login()


    # let's check if response changed from that data being submitted
    response_2 = client.get('/assignments/1')
    other = client.post('/assignments/1', data={
        'course': '',
        'info': 'h',
    })
    assert b'<p>assignment name fields required</p>' in other.data

