# We want to make sure one test is checking for teachers being displayed their version of the Nav
def test_teacher_nav(client, auth):
    auth.login()
    response = client.get('/home')
    assert b'<nav>'
    assert b'<a class="pretty_anchor" href="/courses">Courses</a>' in response.data
    assert b'<a class="pretty_anchor" href="/sessions">Sessions</a>' in response.data


# We want to make sure one test is checking for students being displayed their version of the Nav
def test_student_nav(client, auth):
    auth.login('student@stevenscollege.edu','asdfgh')
    response = client.get('/home')
    assert b'<nav>'
    assert b'<a class="pretty_anchor" href="/my_courses">Courses</a>' in response.data
