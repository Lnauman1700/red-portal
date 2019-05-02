from flask import Flask, request, Blueprint, render_template, g, redirect, url_for, make_response
from . import db
from portal.auth import login_required
bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=('GET', 'POST'))
@login_required
def assignments():
    message = None

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sessions JOIN courses ON sessions.course_id = courses.course_id WHERE courses.teacher_id = %s;", (g.user[0],))
    sessions = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute("""
        SELECT  assignments.assignment_id,
                assignments.assignment_name,
                courses.course_name,
                courses.course_number,
                users.email,
                sessions.letter,
                sessions.session_time,
                sessions.session_id
        FROM courses
        JOIN users ON courses.teacher_id = users.id
        JOIN sessions ON courses.course_id = sessions.course_id
        JOIN assignments ON assignments.session_id = sessions.session_id
        WHERE courses.teacher_id = %s
        ORDER BY
            courses.course_number ASC,
            sessions.letter ASC
    """, (g.user[0],))
    assign = cur.fetchall()
    cur.close()

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

    elif request.method == 'POST':
        assignment_name = request.form['assignment_name']
        info = request.form['info']
        sess_id = request.form.get('sess')
        assignment_type = request.form['type']
        total_points = request.form['points']

        if assignment_name is '' or total_points is '':
            message = 'assignment name and total points fields required'
            return (render_template('assignments.html', message=message, sessions=sessions, assign=assign))

        elif sess_id is '':
            message = 'Session required'
            return (render_template('assignments.html', message=message, sessions=sessions, assign=assign))

        if message is None:
            cur = conn.cursor()
            cur.execute("INSERT INTO assignments (session_id, assignment_name, assignment_info, assignment_type, total_points) VALUES (%s,%s,%s,%s,%s)", (sess_id, assignment_name, info, assignment_type, total_points))
            conn.commit()
            cur.close()

            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT assignment_id FROM assignments ORDER BY assignment_id DESC")
                    recent_assignment_id = cur.fetchone()

            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT users_sessions.student, assignments.assignment_id FROM assignments
                    JOIN sessions ON assignments.session_id = sessions.session_id
                    JOIN users_sessions ON users_sessions.session = sessions.session_id
                    WHERE assignments.assignment_id = %s;
                    """, (recent_assignment_id,))
                    students_submission_data = cur.fetchall()
                    for student in students_submission_data:
                        cur.execute("INSERT INTO submissions (student_id, assignment_id) VALUES (%s, %s)", (student[0], student[1],))
            return redirect(url_for('.assignments'))

    return render_template('assignments.html', message=message, assign=assign, sessions=sessions)


@bp.route('/assignments/<int:id>', methods=('GET', 'POST'))
@login_required
def assignment_update(id):
    conn = db.get_db()

    cur = conn.cursor()
    cur.execute("""
        SELECT  assignments.assignment_id,
                assignments.assignment_name,
                courses.teacher_id,
                courses.course_name,
                courses.course_number,
                users.email,
                sessions.letter,
                sessions.session_time,
                sessions.session_id
        FROM courses
        JOIN users ON courses.teacher_id = users.id
        JOIN sessions ON courses.course_id = sessions.course_id
        JOIN assignments ON assignments.session_id = sessions.session_id
        WHERE courses.teacher_id = %s
    """, (g.user[0],))
    assign = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute("""
        SELECT  assignments.assignment_id,
                assignments.assignment_name,
                assignments.assignment_info,
                courses.teacher_id,
                courses.course_number,
                sessions.letter,
                assignments.total_points
        FROM courses
        JOIN users ON courses.teacher_id = users.id
        JOIN sessions ON courses.course_id = sessions.course_id
        JOIN assignments ON assignments.session_id = sessions.session_id
        WHERE assignments.assignment_id = %s""", (id,))
    assignment= cur.fetchone()
    cur.close()

    message = None

    if request.method == 'GET':
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        elif not assign:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        elif assignment is None:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        elif assignment[3] != g.user[0]:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)

        else:
            return render_template('update_assignments.html', assignment=assignment, message=message)

    elif request.method == 'POST':
        assignment_name = request.form['assignment']
        info = request.form['info']
        assignment_type = request.form['type']
        total_points = request.form['points']

        if assignment_name is '' or total_points is '':
            message = 'assignment name and total points fields required'
            return (render_template('update_assignments.html', message=message, assignment=assignment))

        if message is None:
            cur = conn.cursor()
            cur.execute("UPDATE assignments SET assignment_name = %s, assignment_info = %s, assignment_type = %s, total_points = %s WHERE assignment_id = %s", (assignment_name,info,assignment_type,total_points,id,))
            conn.commit()
            cur.close()
            return redirect(url_for('.assignments'))

    return render_template('update_assignments.html', assignment=assignment, message=message)
