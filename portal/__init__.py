from flask import Flask, render_template
from . import db


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
        return render_template('index.html')

    @app.route('/home')
    def home():
        return render_template('home.html')
        # The code bellow is what was there before I changed it so I could look at the page.
        # return render_template('home.html', user=user)

    return app
