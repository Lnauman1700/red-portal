from flask import Flask, render_template, request, Blueprint, g, redirect, url_for

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
    if request.method == 'GET':
        # display session info
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sessions WHERE session_id = %s", (id,))
        session = cur.fetchone()
        
        # query up the students who aren't in this session, put it in a value
        conn = db.get_db()
        cur = conn.cursor()
        # only include students whose id doesn't show up in the sessions_users junction table under the current session
        cur.execute("SELECT * FROM users WHERE role = 'student'")
        students = cur.fetchall()
        # render the template, send previous value in
        return render_template('session_add.html', session=session, students=students)
            # in the template, the options in the drop-down menu will have value=user id and display email
    elif request.method == 'POST':
        pass
        # grab the value from the post
        # query inserting the user and the session into users_sessions
        # set message that says whether a success or a fail
            # maybe a query that searches for the student/session value in table
        # render same template as in GET request, send in error message
