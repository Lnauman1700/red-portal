from flask import Flask, request, Blueprint, render_template, g, redirect, url_for
from . import db
from portal.auth import login_required
bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=('GET', 'POST'))
@login_required
def courses():
    error = None
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            return redirect(url_for('home'))
    elif request.method == 'POST':
        course_number = request.form['course_number']
        course = request.form['course']
        info = request.form['info']

        if course_number is '' or course is '':
            error = 'Course Number and Course fields required'

        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO courses (teacher_id,course_number,course_name, course_info) VALUES (%s,%s,%s,%s)", (int(g.user[0]),course_number,course,info,))
            conn.commit()

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM courses WHERE teacher_id = %s', (g.user[0],))

    rows = cur.fetchall()

    return render_template('courses.html', rows=rows, error=error)

@bp.route('/courses/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM courses WHERE course_id = %s', (id,))
    course = cur.fetchone()
    error = None
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            return redirect(url_for('home'))
        elif course[1] != g.user[0]:
            return redirect(url_for('.courses'))
        else:
            return render_template('update.html', course=course, error=error)
    elif request.method == 'POST':
        course_number = request.form['course_number']
        course_name = request.form['course']
        info = request.form['info']

        if course_number is '' or course_name is '':
            error = 'Course Number and Course fields required'
        if error is None:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("UPDATE courses SET course_number = %s, course_name = %s, course_info = %s WHERE course_id = %s", (course_number,course_name,info,id))
            conn.commit()
            return redirect(url_for('.courses'))

    return render_template('update.html', course=course, error=error)
    # check that the teacher logged in is the one who owns the course at ID
    # we wanna display form similar or identical to /courses/ route
    # we want it to update the data for this course

    # maybe make a custom error for if they access an ID that doesn't exist?
