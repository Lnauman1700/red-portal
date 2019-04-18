from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from portal.auth import login_required

# Definining the Blueprint and what it's being named
bp = Blueprint('my_courses',__name__)

# adding the app routing to the 'my_courses'page
@bp.route('/my_courses')
def my_courses():
    table_headers = ["Course", "Location", "Instructor", "Time"]

    table = [
        ("CSET 155", "Orange Campus", "Zach Fedor", "MTWRF 12:00pm"),
        ("CSET 160", "Orange Campus", "Zach Fedor", "MTWRF 12:00pm"),
        ("CSET 170", "Orange Campus", "Zach Fedor", "MTWRF 12:00pm"),
        ("CSET 180", "Orange Campus", "Zach Fedor", "MTWRF 12:00pm"),
        ("English Composition", "Mellor", "Patricia Melley", "MWF 9:00am")
    ]

    return render_template('my_courses.html', table=table, table_headers=table_headers)
