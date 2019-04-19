from flask import Flask, render_template, request, Blueprint, g, make_response

from . import db
from portal.auth import login_required

bp = Blueprint('sessions', __name__)

@bp.route('/sessions', methods=['GET'])
@login_required
def sessions_index():
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)
        else:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
            sessions = cur.fetchall()

            return render_template('sessions_list.html', sessions=sessions)

@bp.route('/sessions/<int:id>', methods=['GET', 'POST'])
@login_required
def sessions_add(id):

    message = None

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role = 'student'")
    students = cur.fetchall()

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE sessions.session_id = %s AND courses.teacher_id = %s", (id, g.user[0],))
    session = cur.fetchone()

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)
        else:
            # if session doesn't exist, then throw error
            if session is None:
                message = "Session does not exist"
                return make_response(render_template("error_page.html", message=message), 404)
            else:
                return render_template('session_add.html', session=session, students=students)

    elif request.method == 'POST':
        student_id = int(request.form['student'])

        conn = db.get_db()
        cur = conn.cursor()
        # lists students who are already present in the current session, and the session ID
        cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (student_id, id,))
        already_present = cur.fetchone()

        # check to see if that student is already present in the session
        if already_present is not None:
            message = "Student is already in this session"
            return render_template('session_add.html', message=message, session=session, students=students)
        else:
            # query inserting the user and the session into users_sessions
            cur.execute("INSERT INTO users_sessions VALUES (%s, %s)", (student_id, id,))
            conn.commit()
            message = 'Student successfully added'

        return render_template('session_add.html', session=session, students=students, id=id, message=message)

@bp.route('/sessions/create', methods=['GET', 'POST'])
@login_required
def create_session():

    conn = db.get_db()
    cur = conn.cursor()
    # queries up all of the courses associated with the currently logged in teacher
    cur.execute("SELECT * FROM courses WHERE teacher_id = %s", (g.user[0],))
    courses = cur.fetchall()

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)
        else:
            return render_template('session_create.html', courses=courses)

    elif request.method == 'POST':
        session_letter = request.form['session_letter']
        session_time = request.form['session_time']
        course_id = request.form['course_id']

        if session_letter is "" or session_time is "" or course_id is "":
            message = "Please complete entire form"
            return render_template('session_create.html', error=error, message=message)
        else:
            conn = db.get_db()
            cur = conn.cursor()
            # create a new session using the form data
            cur.execute("INSERT INTO sessions (letter, session_time, course_id) VALUES (%s, %s, %s)", (session_letter, session_time, course_id))
            conn.commit()
            message = "Session successfuly created"
            return render_template('session_create.html', message=message, courses=courses)
