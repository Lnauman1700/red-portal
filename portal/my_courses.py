from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

# Definining the Blueprint and what it's being named
bp = Blueprint('my_courses',__name__)

# adding the app routing to the 'my_courses'page
@bp.route('/my_courses')
def my_courses():
    return render_template('my_courses.html')
