from flask import Flask, render_template, request, Blueprint, g, make_response, redirect, url_for

from . import db
from portal.auth import login_required

bp = Blueprint('add_grades', __name__)

@bp.route('/assignments/<int:assignment_id>/grades', methods=['GET', 'POST'])
@login_required
def grades(assignment_id):

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT courses.teacher_id, assignments.assignment_id, courses.course_number, sessions.letter, assignments.assignment_name, assignments.total_points FROM assignments JOIN sessions ON assignments.session_id = sessions.session_id JOIN courses ON courses.course_id = sessions.course_id WHERE assignments.assignment_id = %s", (assignment_id,))
            assignment = cur.fetchone()
    if request.method == 'GET':
        # make sure user accessing it is a teacher, and owns the course related to the assignment
        if g.user[3] != 'teacher':
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)
        elif assignment is None:
            message = 'Page does not exist'
            return make_response(render_template('error_page.html', message=message), 404)
        elif g.user[0] != assignment[0]:
            message = 'You are not permitted to view this page'
            return make_response(render_template('error_page.html', message=message), 401)
        else:
            # grab students in assignment's session, eventually we'll list them out in the HTML
            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT submissions.student_id, users.email, submissions.points FROM submissions
                    JOIN assignments ON submissions.assignment_id = assignments.assignment_id
                    JOIN users ON submissions.student_id = users.id
                    WHERE assignments.assignment_id = %s;
                    """, (assignment_id,))
                    students = cur.fetchall()
            # if there are no submissions yet, just get a list of the students
            if students == []:
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT users_sessions.student, users.email FROM users JOIN users_sessions ON users.id = users_sessions.student JOIN sessions ON sessions.session_id = users_sessions.session JOIN assignments ON sessions.session_id = assignments.session_id WHERE assignments.assignment_id = %s", (assignment_id,))
                        students = cur.fetchall()

            return render_template('add_grades.html', students=students, assignment=assignment)
    if request.method == 'POST':
        # query all students in this session
        with db.get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT users_sessions.student, users.email FROM users JOIN users_sessions ON users.id = users_sessions.student JOIN sessions ON sessions.session_id = users_sessions.session JOIN assignments ON sessions.session_id = assignments.session_id WHERE assignments.assignment_id = %s", (assignment_id,))
                students = cur.fetchall()
        # for each student in this session, grab their student id from the db
        for student in students:
            # check that the id is in the request.form
            student_grade = request.form[f'{student[0]}']
            # if there's already a submission for the user in the assignment, let's update it
            with db.get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT submissions.student_id, submissions.assignment_id FROM users JOIN users_sessions ON users.id = users_sessions.student JOIN sessions ON sessions.session_id = users_sessions.session JOIN assignments ON sessions.session_id = assignments.session_id JOIN submissions ON submissions.assignment_id = assignments.assignment_id WHERE submissions.assignment_id = %s AND submissions.student_id = %s", (assignment_id, student[0],))
                    submission = cur.fetchone()
            if submission is None:
                # make sure there was info sent through the form, if there wasn't then account for that
                if student_grade == "":
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO submissions (assignment_id, student_id) VALUES (%s, %s)", (assignment_id, student[0]))
                else:
                    letter_grade = get_letter(student_grade, assignment[5])
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO submissions (assignment_id, student_id, points, letter) VALUES (%s, %s, %s, %s)", (assignment_id, student[0], student_grade, letter_grade,))
            # if it's in the request.form and there isn't already data for it, we'll make a new submission
            else:
                if student_grade == "":
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE submissions SET points = %s, letter = %s WHERE student_id = %s AND assignment_id = %s", (None, None, student[0], assignment_id,))
                else:
                    letter_grade = get_letter(student_grade, assignment[5])
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE submissions SET points = %s, letter = %s WHERE student_id = %s AND assignment_id = %s", (student_grade, letter_grade, student[0], assignment_id,))

        # queries updated student info to send in to the page again
        with db.get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT submissions.student_id, users.email, submissions.points FROM submissions
                JOIN assignments ON submissions.assignment_id = assignments.assignment_id
                JOIN users ON submissions.student_id = users.id
                WHERE assignments.assignment_id = %s;
                """, (assignment_id,))
                students = cur.fetchall()

        return render_template('add_grades.html', students=students, assignment=assignment)


def get_letter(points, total):
    fraction = int(points)/total
    if fraction >= 0.90:
        return 'A'
    elif fraction >= 0.80:
        return 'B'
    elif fraction >= 0.70:
        return 'C'
    elif fraction >= 0.60:
        return 'D'
    else:
        return 'F'
