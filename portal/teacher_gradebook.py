from flask import Blueprint, g, render_template, make_response
from portal.auth import login_required
from . import db

bp = Blueprint('gradebook',__name__)

@bp.route('/gradebook')
@login_required
def gradebook():

    # with db.get_db() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute()

    return render_template('teacher_gradebook.html')
