from flask import Flask, render_template, request, Blueprint, g, make_response

from . import db
from portal.auth import login_required

bp = Blueprint('add_grades', __name__)

@bp.route('/assignments/<int:assignment_id>/grades', methods=['GET', 'POST'])
@login_required
def grades(assignment_id):
    # TODO
    # GET
        # make sure user accessing it is a teacher
        # make sure assignment id exists, teacher accessing it owns it
        # grab students in assignment's session, eventually we'll list them out in the HTML
    # POST
        # get the data relating to each student's grade
        # do something with the unentered ones
        # make sure student's grade isn't already entered, if it is, update it
        # add into the DB the grades, student associated with them, ect


    return render_template('add_grades.html')
