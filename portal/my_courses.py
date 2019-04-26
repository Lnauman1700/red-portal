from flask import Blueprint, g, render_template, make_response
from portal.auth import login_required
from . import db

# Definining the Blueprint and what it's being named
bp = Blueprint('my_courses',__name__)

# adding the app routing to the 'my_courses'page
@bp.route('/my_courses')
@login_required
def my_courses():
    if g.user[3] == 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    table_headers = ["Course", "Instructor", "Time"]

    conn = db.get_db()
    cur = conn.cursor()
    # currently logged in user's sessions should be displayed
    # we should display the course number and course name as well
    # display who the teacher is as well
    cur.execute("""
        SELECT courses.course_name, courses.course_number, sessions.letter, users.email, sessions.session_time, users_sessions.student
        FROM courses
        JOIN sessions ON courses.course_id = sessions.course_id
        JOIN users ON courses.teacher_id = users.id
        JOIN users_sessions ON sessions.session_id = users_sessions.session
        WHERE users_sessions.student = %s;
    """, (g.user[0],))
    table = cur.fetchall()
    print(table)

    return render_template('my_courses.html', table=table, table_headers=table_headers)
