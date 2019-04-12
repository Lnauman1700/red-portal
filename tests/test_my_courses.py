def test_my_courses(client):
    response = client.get('/my_courses')
    assert b'<h1>My Courses</h1>' in response.data
    assert 200 == response.status_code
    assert b'<article>' in response.data
    assert b'<table>' in response.data
    assert b'<tr>' in response.data
    assert b'th>Course Name</th>' in response.data
    assert b'<th>Location</th>' in response.data
    assert b'<th>Instructor</th>' in response.data
    assert b'<th>Time</th>' in response.data
