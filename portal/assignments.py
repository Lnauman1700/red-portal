from flask import Flask, request, Blueprint, render_template, g, redirect, url_for, make_response
from . import db
from portal.auth import login_required
bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=('GET', 'POST'))
@login_required
def assignments():
    error = None

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions JOIN courses ON sessions.session_id = courses.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
    sessions = cur.fetchall()
    cur.close()


    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments JOIN courses ON assignments.session_id = courses.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
    assign = cur.fetchall()
    cur.close()

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)  

    elif request.method == 'POST':
        assignment_name = request.form['assignment_name']
        info = request.form['info']
        sess_id = request.form['session']
        if assignment_name is '':
            error = 'assignment name fields required'
        
        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO assignments (session_id, assignment_name, assignment_info) VALUES (%s,%s,%s)", (sess_id, assignment_name, info,))
            conn.commit()
            cur.close()
            return redirect(url_for('.assignments'))
    return render_template('assignments.html', error=error, assign=assign, sessions=sessions)

@bp.route('/assignments/<int:id>', methods=('GET', 'POST'))
@login_required
def assignment_update(id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments WHERE assignment_id = %s', (id,))
    assignment = cur.fetchone()
    cur.close()


    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments JOIN courses ON assignments.session_id = courses.course_id WHERE assignments.assignment_id = %s;", (id,))
    assign = cur.fetchone()
    cur.close()

    error = None
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        elif not assign:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        elif assign[5] != g.user[0]:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        else:
            return render_template('update_assignments.html', assignment=assignment, error=error)

    elif request.method == 'POST':
        assignment_name = request.form['assignment']
        info = request.form['info']

        if assignment is '':
            error = 'assignment name fields required'

        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("UPDATE assignments SET assignment_name = %s, assignment_info = %s WHERE assignment_id = %s", (assignment_name,info,id))
            conn.commit()
            cur.close()
            return redirect(url_for('.assignments'))
            
    return render_template('update_assignments.html', assignment=assignment, error=error)
