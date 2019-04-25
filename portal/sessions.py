from flask import Flask, render_template, request, Blueprint, g, redirect, url_for, make_response

from . import db
from portal.auth import login_required

bp = Blueprint('sessions', __name__)

@bp.route('/sessions', methods=['GET'])
@login_required
def sessions_index():
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            error = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', error=error), 401)
        else:
            # once courses is established, check that g.user is teacher
            # access sessions (based on teacher in g.user), put them into a variable
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
            sessions = cur.fetchall()
            # render template, send in previously mentioned value
            return render_template('sessions_list.html', sessions=sessions)

@bp.route('/sessions/<int:id>', methods=['GET', 'POST'])
@login_required
def sessions_add(id):

    error = None

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role = 'student'")
    students = cur.fetchall()

    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE sessions .session_id = %s AND courses.teacher_id = %s", (id, g.user[0],))
    session = cur.fetchone()

    if request.method == 'GET':
        # display session info
        if g.user[3] != 'teacher':
            error = 'You are not permitted to view this page'
            return render_template('error_page.html', error=error)
        else:
            # if session doesn't exist, then throw error
            if session is None:
                error = "Session does not exist"
                return make_response(render_template("error_page.html", error=error), 404)
            else:
                # query up the students who aren't in this session, put it in a value
                # render the template, send previous value in
                return render_template('session_add.html', session=session, students=students)
                    # in the template, the options in the drop-down menu will have value=user id and display email
    elif request.method == 'POST':
        # grab the value from the post
        student_id = int(request.form['student'])

        cur = conn.cursor()
        cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (student_id, id,))
        already_present = cur.fetchone()

        if already_present is not None:
            error = "Student is already in this session"
            return render_template('session_add.html', error=error, session=session, students=students)
        else:
            # query inserting the user and the session into users_sessions
            cur.execute("INSERT INTO users_sessions VALUES (%s, %s)", (student_id, id,))
            conn.commit()
            error = 'Student successfully added'
        # set message that says whether a success or a fail

            # maybe a query that searches for the student/session value in table
        # render same template as in GET request, send in error message
        return render_template('session_add.html', session=session, students=students, id=id, error=error)

@bp.route('/sessions/create', methods=['GET', 'POST'])
@login_required
def create_session():

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses WHERE teacher_id = %s", (g.user[0],))
    courses = cur.fetchall()

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            error = 'You are not permitted to view this page'
            return render_template('error_page.html', error=error)
        else:
            return render_template('session_create.html', courses=courses)

    elif request.method == 'POST':
        session_letter = request.form['session_letter']
        session_time = request.form['session_time']
        course_id = request.form['course_id']

        if session_letter is "" or session_time is "" or course_id is "":
            error = "Please complete entire form"
            return render_template('session_create.html', error=error, courses=courses)
        else:
            cur = conn.cursor()
            cur.execute("INSERT INTO sessions (letter, session_time, course_id) VALUES (%s, %s, %s)", (session_letter, session_time, course_id))
            conn.commit()
            success = "Session successfully created"
            return render_template('session_create.html', success=success, courses=courses)
