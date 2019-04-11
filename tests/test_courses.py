
def test_courses(client):
    # assert client.get('/courses').status_code == 200
    response = client.get('/courses')
    assert 200 == response.status_code
    assert b'<h1>Courses</h1>' in response.data
