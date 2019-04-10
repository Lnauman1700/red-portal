from flask import Flask, render_template, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        if request.method == 'POST':

            email  = request.form['email']
            password  = request.form['password']

            dab = db.get_db()
            cur = dab.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
            user = cur.fetchone()

            if password == user[2]:
                # store user info in a session
                return render_template('home.html')
            else:
                return render_template('index.html')
        else:
            return render_template('index.html')

    @app.route('/home')
    def home():
        return render_template('home.html', user=user)

    return app
