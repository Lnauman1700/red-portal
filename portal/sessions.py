from flask import Flask, render_template, request, Blueprint, g, redirect, url_for, make_response

from . import db

bp = Blueprint('sessions', __name__)

@bp.route('/sessions', methods=['GET'])
def sessions_index():
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            error = 'You are not permitted to view this page'
            return redirect(url_for('home'))
        else:
            # once courses is established, check that g.user is teacher
            # access sessions (based on teacher in g.user), put them into a variable
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sessions")
            sessions = cur.fetchall()
            # render template, send in previously mentioned value
            return render_template('sessions_list.html', sessions=sessions)

@bp.route('/sessions/<int:id>', methods=['GET', 'POST'])
def sessions_add(id):

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role = 'student'")
    students = cur.fetchall()

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions WHERE session_id = %s", (id,))
    session = cur.fetchone()

    if request.method == 'GET':
        # display session info

        # if session doesn't exist, then return us to the sessions list page
        if session is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM sessions")
            sessions = cur.fetchall()
            return make_response(render_template("sessions_list.html", sessions=sessions), 404)
        else:
            # query up the students who aren't in this session, put it in a value
            # render the template, send previous value in
            return render_template('session_add.html', session=session, students=students)
                # in the template, the options in the drop-down menu will have value=user id and display email
    elif request.method == 'POST':
        # grab the value from the post
        student_id = int(request.form['student'])

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (student_id, id,))
        already_present = cur.fetchone()

        if already_present is not None:
            print("we already have this student in")
        else:
            # query inserting the user and the session into users_sessions
            cur.execute("INSERT INTO users_sessions VALUES (%s, %s)", (student_id, id,))
            conn.commit()
            print("Student added")
        # set message that says whether a success or a fail

            # maybe a query that searches for the student/session value in table
        # render same template as in GET request, send in error message
        return redirect(url_for('sessions.sessions_add', session=session, students=students, id=id))

@bp.route('/sessions/create')
