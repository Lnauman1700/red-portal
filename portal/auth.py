from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, g
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        email  = request.form['email']
        password  = request.form['password']

        if email is None or password is None:
            return render_template('index.html')
        else:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
            user = cur.fetchone()

            if user is None:
                session.clear()
                session['user_id'] = None
                return redirect(url_for('index'))
            # utilize hashes and compare hashed password to password in DB
            elif not check_password_hash(user[2], password):
            # store user info in a session
                session.clear()
                session['user_id'] = None
                return redirect(url_for('index'))
            else:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('home'))
    else:
        session['user_id'] = None
        print(session['user_id'])
        return render_template('index.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def get_current_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        g.user = cur.fetchone()
