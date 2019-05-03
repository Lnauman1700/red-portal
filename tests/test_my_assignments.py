from io import BytesIO

def test_validation_my_assignments(client, auth):
    with client:
        response = client.get('/my_assignments/2')
        assert response.headers['Location'] == 'http://localhost/'
    with client:
        auth.login("student_2@stevenscollege.edu", "x")
        response = client.get('/my_assignments/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login()
        response = client.get('/my_assignments/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        response = client.get('/my_assignments/2')
        assert response.status_code == 200
        assert b'CSET 155B' in response.data
        response = client.get('/my_assignments/100')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data

def test_view_assignments(client, auth):
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        response = client.get('/my_assignments/2')
        assert b'Delete Database' in response.data

def test_validation_assignment_description(client, auth):
    with client:
        response = client.get('/my_assignments/assignment_description/2')
        assert response.headers['Location'] == 'http://localhost/'
    with client:
        auth.login("student_2@stevenscollege.edu", "x")
        response = client.get('/my_assignments/assignment_description/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login()
        response = client.get('/my_assignments/assignment_description/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        response = client.get('/my_assignments/assignment_description/2')
        assert response.status_code == 200
        assert b'Delete Database' in response.data
        assert b'Work with postgres SQL' in response.data
        response = client.get('/my_assignments/assignment_description/100')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data

def test_uploads(client, auth):
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        data = {
        'file': (BytesIO(b'FILE CONTENT'), 'test.txt')
        }
        response = client.post('/my_assignments/assignment_description/2', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert b'file successfully uploaded' in response.data
        data = {
        'file': (BytesIO(b'FILE CONTENT'), 'test.txt')
        }
        response = client.post('/my_assignments/assignment_description/2', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert b'already submitted assignment' in response.data
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        data = {
        'file': (BytesIO(b'FILE CONTENT'), '')
        }
        response = client.post('/my_assignments/assignment_description/2', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert b'Please put a file in' in response.data
