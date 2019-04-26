from flask import Blueprint, g, render_template, make_response
from portal.auth import login_required
from . import db

#X# Only going being taken to the assignments page that belongs to that course session
## User is only seeing content that belongs to them


# Definining the Blueprint and what it's being named
bp = Blueprint('my_assignments',__name__)

# adding the app routing to the 'my_courses'page
@bp.route('/my_assignments/<int:id>')
@login_required
def my_assignments(id):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT courses.course_name, courses.course_number, sessions.letter, sessions.session_id  FROM courses JOIN sessions ON courses.course_id = sessions.course_id WHERE sessions.session_id = %s', (id,))
    course_info = cur.fetchone()

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users_sessions WHERE student = %s AND session = %s', (g.user[0], id,))
    auth = cur.fetchone()
    error = None
    # This is just to make sure this page is only viewable to student users
    if g.user[3] == 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    elif auth == None:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    table_headers = ["Assignment", "Due", "Grade"]

    return render_template('my_assignments.html', course_info=course_info, table_headers=table_headers)
