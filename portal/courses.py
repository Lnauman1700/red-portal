from flask import Flask, request, Blueprint, render_template, g, redirect, url_for
from . import db
bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=('GET', 'POST'))
def courses():
    if request.method == 'GET':
        if g.user[3] != 'teacher':
            return redirect(url_for('home'))
    elif request.method == 'POST':
        course_number = request.form['course_number']
        course = request.form['course']
        info = request.form['info']
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO courses (teacher_id,course_number,course_name, course_info) VALUES (%s,%s,%s,%s)", (int(g.user[0]),course_number,course,info,))
        conn.commit()
    return render_template('courses.html')