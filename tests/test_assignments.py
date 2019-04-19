from flask import request
def test_assignments_route(client, auth):
    with client:
        auth.login()
        response = client.get('/assignments')
        assert 200 == response.status_code
        assert b'<h1>Assignments</h1>' in response.data
        assert b"<form method='POST'>" in response.data
