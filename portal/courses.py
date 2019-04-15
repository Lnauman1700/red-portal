from flask import Flask, request, Blueprint, render_template

bp = Blueprint('courses', __name__, url_prefix='/courses')

@bp.route('/', methods=('GET', 'POST'))
def courses():
    other=''
    if request.method == 'POST':
        course = request.form['course']
        info = request.form['info']
        other = 'cats'
        print(course)
        print(info)
    return render_template('courses.html', thing=other)