from flask import request
def test_courses(client, auth):
    auth.login()
    response = client.get('/courses')
    assert 200 == response.status_code
    assert b'<h1>Courses</h1>' in response.data
    assert b"<form method='POST'>" in response.data

def test_update(client, auth):
    