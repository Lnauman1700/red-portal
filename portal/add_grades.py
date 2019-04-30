from flask import Flask, render_template, request, Blueprint, g, make_response, redirect, url_for

from . import db
from portal.auth import login_required

bp = Blueprint('add_grades', __name__)

@bp.route('/assignments/<int:assignment_id>/grades', methods=['GET', 'POST'])
@login_required
def grades(assignment_id):

    with db.get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT courses.teacher_id, assignments.assignment_id, courses.course_number, sessions.letter, assignments.assignment_name FROM assignments JOIN sessions ON assignments.session_id = sessions.session_id JOIN courses ON courses.course_id = sessions.course_id WHERE assignments.assignment_id = %s", (assignment_id,))
            assignment = cur.fetchone()
    # GET
    if request.method == 'GET':
        # make sure user accessing it is a teacher
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
            if students == []:
                with db.get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT users_sessions.student, users.email FROM users JOIN users_sessions ON users.id = users_sessions.student JOIN sessions ON sessions.session_id = users_sessions.session JOIN assignments ON sessions.session_id = assignments.session_id WHERE assignments.assignment_id = %s", (assignment_id,))
                        students = cur.fetchall()

            return render_template('add_grades.html', students=students, assignment=assignment)
        # make sure assignment id exists, teacher accessing it owns it
    # POST
    if request.method == 'POST':
        with db.get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT users_sessions.student, users.email FROM users JOIN users_sessions ON users.id = users_sessions.student JOIN sessions ON sessions.session_id = users_sessions.session JOIN assignments ON sessions.session_id = assignments.session_id WHERE assignments.assignment_id = %s", (assignment_id,))
                students = cur.fetchall()
        # query all students in this session
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
                if student_grade == "":
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO submissions (assignment_id, student_id) VALUES (%s, %s)", (assignment_id, student[0]))
                else:
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO submissions (assignment_id, student_id, points) VALUES (%s, %s, %s)", (assignment_id, student[0], student_grade,))
            # if it's in the request.form and there isn't already data for it, we'll make a new submission
            else:
                if student_grade == "":
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE submissions SET points = %s WHERE student_id = %s AND assignment_id = %s", (None, student[0], assignment_id,))
                else:
                    with db.get_db() as conn:
                        with conn.cursor() as cur:
                            cur.execute("UPDATE submissions SET points = %s WHERE student_id = %s AND assignment_id = %s", (student_grade, student[0], assignment_id,))

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


        # get the data relating to each student's grade
        # do something with the unentered ones
        # make sure student's grade isn't already entered, if it is, update it
        # add into the DB the grades, student associated with them, ect
