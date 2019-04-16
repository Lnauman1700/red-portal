from flask import Flask, render_template, request, Blueprint, g

from . import db

bp = Blueprint('sessions', __name__)

@bp.route('/sessions', methods=['GET'])
def sessions_index():
    if request.method == 'GET':
        # once courses is established, check that g.user is teacher
        # access sessions (based on teacher in g.user), put them into a variable
        # render template, send in previously mentioned value

@bp.route('/sessions/<int:id>', methods=['GET', 'POST'])
def sessions_add(id):
    if request.method == 'GET':
        # display session info
        # query up the students who aren't in this session, put it in a value
        # render the template, send previous value in
            # in the template, the options in the drop-down menu will have value=user id and display email
    elif request.method == 'POST':
        # grab the value from the post
        # query inserting the user and the session into users_sessions
        # set message that says whether a success or a fail
            # maybe a query that searches for the student/session value in table
        # render same template as in GET request, send in error message
