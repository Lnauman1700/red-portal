from flask import Flask, request, Blueprint, render_template, g, redirect, url_for
from . import db
from portal.auth import login_required
bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=('GET', 'POST'))
@login_required
def assignments():
    error = None
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            return redirect(url_for('home'))

    elif request.method == 'POST':
        assignment_name = request.form['assignment_name']
        info = request.form['info']

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT course_id FROM assignments WHERE course_id = %s', (course_id,))
        course_id = cur.fetchone()
        
        if assignment_name is '':
            error = 'assignment name fields required'
        
        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO assignments (course_id, assignment_info) VALUES (%s,%s,%s,%s)", (course_id,assignment_name,info,))
            conn.commit()

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments WHERE course_id = %s', (g.user[0],))

    rows = cur.fetchall()

    return render_template('assignments.html', rows=rows, error=error)

@bp.route('/assignments/<int:id>', methods=('GET', 'POST'))
@login_required
def assignment_update(id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM assignments WHERE assignment_id = %s', (id,))
    assignment = cur.fetchone()
    error = None
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            return redirect(url_for('home'))

        elif assignment == None:
            return redirect(url_for('.assignments'))

        elif assignment[1] != g.user[0]:
            return redirect(url_for('.assignments'))

        else:
            return render_template('update.html', assignment=assignment, error=error)

    elif request.method == 'POST':
        assignment_number = request.form['assignment_number']
        assignment_name = request.form['assignment']
        info = request.form['info']

        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT assignment_id, assignment_number FROM assignments WHERE assignment_number = %s', (assignment_number,))
        assignment_data = cur.fetchone()

        if assignment_data is not None:
            if assignment_data[0] != id:
                error = 'assignment number already exists'

        elif assignment_number is '' or assignment is '':
            error = 'assignment Number and assignment fields required'

        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("UPDATE assignments SET assignment_number = %s, assignment_name = %s, assignment_info = %s WHERE assignment_id = %s", (assignment_number,assignment_name,info,id))
            conn.commit()
            return redirect(url_for('.assignments'))

    return render_template('update.html', assignment=assignment, error=error)
