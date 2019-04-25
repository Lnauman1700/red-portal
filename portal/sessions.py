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
            # all of the sessions/create html stuff goes into here
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
            sessions = cur.fetchall()
            # display a list of sessions so you can eventually edit them

            return render_template('sessions_list.html', sessions=sessions)
    # add sessions/create POST request stuff into here

@bp.route('/sessions/<int:id>', methods=['GET', 'POST'])
@login_required
def sessions_add(id):

    message = None

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT sessions.letter, sessions.session_time, courses.course_number FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE sessions.session_id = %s AND courses.teacher_id = %s", (id, g.user[0],))
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
                return render_template('session_add.html', session=session)

    elif request.method == 'POST':
        session_letter = request.form['session_letter']
        session_time = request.form['session_time']
        students = request.form.getlist('student')

        if session_letter is "" or session_time is "" or "" in students:
            message = "Please complete entire form"
            return render_template('session_add.html', session=session, message=message)
        elif len(session_letter) > 1:
            message = "Form was incorrectly filled out"
            return render_template('session_add.html', session=session, message=message)
        else:
            message = ''
            # check that all students who are in students list are actual students, or that they're not already in
            for student in students:
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT * FROM users WHERE email = %s AND role = 'student'", (student,))
                        studentValue = cur.fetchone()
                        if studentValue is None:
                            message = f'A student with the email {student} does not exist'
                            break

            # update session using form data
            if 'A student with the email' not in message:
                session_id = ''
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE sessions SET letter = %s, session_time = %s WHERE session_id = %s", (session_letter, session_time, id))
                        conn.commit()
                message = "Session successfuly updated"
                # add the students to the newly-made session (query up the session id of the recently added session)
                for student in students:
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            # grab student's id
                            cur.execute("SELECT id FROM users WHERE email = %s", (student,))
                            student_id = cur.fetchone()
                            # check that this student isn't already in the session
                            cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (student_id, id))
                            already_added = cur.fetchone()
                            # if student isn't in this session, add them in
                            if already_added is None:
                                cur.execute("INSERT INTO users_sessions VALUES (%s, %s)", (student_id[0], id))
                                conn.commit()

            return render_template('session_add.html', session=session, message=message)


@bp.route('/sessions/create', methods=['GET', 'POST'])
@login_required
def create_session():

    conn = db.get_db()
    cur = conn.cursor()
    # queries up all of the courses associated with the currently logged in teacher
    cur.execute("SELECT * FROM courses WHERE teacher_id = %s;", (g.user[0],))
    courses = cur.fetchall()
    cur.close()

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
        students = request.form.getlist('student')

        if course_id is "" or session_letter is "" or session_time is "" or "" in students:
            message = "Please complete entire form"
            return render_template('session_create.html', courses=courses, message=message)
        elif len(session_letter) > 1:
            message = "Form was incorrectly filled out"
            return render_template('session_create.html', courses=courses, message=message)
        else:
            message = ''
            # check that all students who are in students list are actual students
            for student in students:
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT * FROM users WHERE email = %s AND role = 'student'", (student,))
                        studentValue = cur.fetchone()
                        if studentValue is None:
                            message = f'A student with the email {student} does not exist'
                            break
            # create a new session using the form data
            if 'A student with the email' not in message:
                session_id = ''
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO sessions (letter, session_time, course_id) VALUES (%s, %s, %s)", (session_letter, session_time, course_id))
                        conn.commit()
                        cur.execute("SELECT session_id FROM sessions ORDER BY session_id DESC")
                        session_id = cur.fetchone()
                message = "Session successfuly created"
                # add the students to the newly-made session (query up the session id of the recently added session)
                for student in students:
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            # grab student's id
                            cur.execute("SELECT id FROM users WHERE email = %s", (student,))
                            student_id = cur.fetchone()
                            # check that this student isn't already in the session
                            cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (student_id, session_id))
                            already_added = cur.fetchone()
                            # if student isn't in this session, add them in
                            if already_added is None:
                                cur.execute("INSERT INTO users_sessions VALUES (%s, %s)", (student_id[0], session_id))
                                conn.commit()


            return render_template('session_create.html', message=message, courses=courses)
