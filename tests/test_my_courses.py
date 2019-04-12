def test_my_courses(client):
    response = client.get('/my_courses')
    assert b'<h1>My Courses</h1>' in response.data
    assert 200 == response.status_code
