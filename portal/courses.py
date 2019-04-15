from flask import Flask, request, Blueprint, render_template

bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=('GET', 'POST'))
def courses():
    if request.method == 'POST':
        course_number = request.form['course_number']
        course = request.form['course']
        info = request.form['info']
        print(course)
        print(course_number)
        print(info)
    return render_template('courses.html')