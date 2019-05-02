from flask import Blueprint, g, render_template, make_response, request, url_for
import os
from portal.auth import login_required
from . import db, __init__

bp = Blueprint('my_assignments',__name__)

@bp.route('/my_assignments/<int:id>')
@login_required
def my_assignments(id):

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT courses.course_name, courses.course_number, sessions.letter, sessions.session_id  FROM courses JOIN sessions ON courses.course_id = sessions.course_id WHERE sessions.session_id = %s', (id,))
            course_info = cur.fetchone()

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (g.user[0], id,))
            auth = cur.fetchone()

    # Write query to access all grades specific to student ID and session  ID for average

    # with db.get_db() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute("SELECT * FROM grades WHERE student_id = %s AND session_id = %s", (g.user[0], id,))
    #         all_grades = cur.fetchall()

    if course_info == None:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    #join grades table to display grades for specific assignments
    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM assignments WHERE session_id = %s", (course_info[3],))
            assign_info = cur.fetchall()

    if auth == None:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    elif g.user[3] == 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    table_headers = ["Assignment", "Grade"]

    return render_template('my_assignments.html', course_info=course_info, table_headers=table_headers, assign_info=assign_info)


@bp.route('/my_assignments/assignment_description/<int:id>', methods = ['GET', 'POST'])
@login_required
def assignment_description(id):

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM assignments where assignment_id = %s", (id,))
            assignment_desc = cur.fetchone()

    if assignment_desc == None:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users_sessions WHERE student = %s AND session = %s", (g.user[0], assignment_desc[1],))
            auth = cur.fetchone()

    if g.user[3] == 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    elif auth == None:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    elif request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join("portal/uploads", file.filename))

        with db.get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM submissions WHERE assignment_id = %s AND student_id = %s", (id, g.user[0],))
                submission = cur.fetchone()
        if submission is None:
            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO submissions (assignment_id, student_id, filename) VALUES (%s, %s, %s)", (id, g.user[0], file.filename,))
        else:
            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE submissions SET filename = %s WHERE assignment_id = %s AND student_id = %s", (file.filename, id, g.user[0],))
        message = "file successfully uploaded"
        file = "file"
        return render_template("assignment_description.html", assignment_desc=assignment_desc, file=file, message=message)

    elif assignment_desc[4] == "file":
        file = 'hey'
        return render_template('assignment_description.html', assignment_desc=assignment_desc, file=file)


    return render_template('assignment_description.html', assignment_desc=assignment_desc)
