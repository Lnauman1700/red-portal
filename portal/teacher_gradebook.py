from flask import Blueprint, g, render_template, make_response, request
from portal.auth import login_required
from . import db

bp = Blueprint('gradebook',__name__)

@bp.route('/gradebook')
@login_required
def gradebook():
        
    if g.user[3] != 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT sessions.session_id,
                    courses.course_name,
                    courses.course_number,
                    sessions.letter,
                    courses.teacher_id
            FROM sessions
            JOIN courses ON courses.course_id = sessions.course_id
            WHERE courses.teacher_id = %s""", (g.user[0],))
            sess_info = cur.fetchall()

    table_header =  ['Course Sessions']

    return render_template('teacher_gradebook.html', sess_info=sess_info, table_header=table_header)

@bp.route('/gradebook/<int:id>')
@login_required
def gradebook_view(id):
    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT courses.teacher_id FROM sessions JOIN courses ON courses.course_id = sessions.course_id WHERE sessions.session_id = %s', (id,))
            session = cur.fetchone()

    if g.user[3] != 'teacher':
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    elif session is None:
        message = 'This Page does not exist'
        return make_response(render_template('error_page.html', message=message), 404)

    elif session[0] != g.user[0]:
        message = 'You are not permitted to view this page'
        return make_response(render_template('error_page.html', message=message), 401)

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users_sessions JOIN users ON users_sessions.student = users.id WHERE session = %s', (id,))
            students_in_session = cur.fetchall()
    grades_list = []
    final_grade = ""
    with db.get_db() as conn:
        with conn.cursor() as cur:
            for students in students_in_session:
                cur.execute("""
                SELECT submissions.points, assignments.total_points, sessions.session_id, users.email
                FROM submissions
                JOIN assignments ON assignments.assignment_id = submissions.assignment_id
                JOIN sessions ON sessions.session_id = assignments.session_id
                JOIN users ON users.id = submissions.student_id
                WHERE submissions.student_id = %s AND sessions.session_id = %s;""",(students[0], id))
                grade_info = cur.fetchall()
                # get total up every grade in grade_info
                points_earned = 0
                points_total = 0
                for grade in grade_info:
                        print(grade)
                        if grade[0]:
                                points_earned += grade[0]
                                points_total += grade[1]
                if points_total == 0:
                        final_grade = "None"
                else:
                        final_grade  = "{0:.0%}".format((points_earned/points_total))
                        
                grades_list.append([students[3], final_grade])

        table_header =  ["Student", "Grade"]

    return render_template('teacher_gradebook_view.html', grades_list=grades_list, table_header=table_header)
