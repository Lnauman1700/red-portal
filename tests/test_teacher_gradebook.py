def test_authentication(client, auth):
    with client:
        auth.login()
        response = client.get('/gradebook/98')
        assert b'This Page does not exist' in response.data
        assert response.status_code == 404
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/gradebook')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401
        response = client.get('/gradebook/1')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data
        assert response.status_code == 401

def test_grades(client, auth):
    auth.login()
    response = client.get('/gradebook/1')
    assert b'student@stevenscollege.edu' in  response.data
    assert b'100%' in response.data

    response = client.post('/assignments/1/grades', data={
        2: ""
    })

    response = client.get('/gradebook/1')
    assert b'student@stevenscollege.edu' in  response.data
    assert b'None' in response.data
