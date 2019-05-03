from flask import Blueprint, g, render_template, make_response
from portal.auth import login_required
from . import db

bp = Blueprint('gradebook',__name__)

@bp.route('/gradebook')
@login_required
def gradebook():

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
            # cur.execute("""
            # SELECT *
            # FROM users
            # JOIN users_sessions ON users.id = users_sessions.student
            # JOIN sessions ON users_sessions.session = sessions.session_id
            # JOIN assignments ON assignments.session_id = sessions.session_id
            # JOIN submissions ON submissions.assignment_id = assignments.assignment_id
            # WHERE sessions.session_id = %s""", (id,))
            # grade_info = cur.fetchall()
            cur.execute("""
            SELECT submissions.points, assignments.total_points, sessions.session_id FROM submissions
            JOIN assignments ON assignments.assignment_id = submissions.assignment_id
            JOIN sessions ON sessions.session_id = assignments.session_id
            WHERE submissions.student_id = %s;
            """, ())
            student_grades = cur.fetchall()

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT submissions.points, assignments.total_points, sessions.session_id, users.email
            FROM submissions
            JOIN assignments ON assignments.assignment_id = submissions.assignment_id
            JOIN sessions ON sessions.session_id = assignments.session_id
            JOIN users ON users.id = submissions.student_id
            WHERE submissions.student_id = %s;""",())

    table_header =  ["Student", "Grade"]

    return render_template('teacher_gradebook_view.html', grade_info=grade_info, table_header=table_header)
