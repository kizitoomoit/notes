import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db, User

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/sign_up', methods=('GET', 'POST'))
    def sign_up():
        if request.method =='POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken.'

            if error is None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))

            flash(error, 'error')








        return render_template('sign_up.html')
    @app.route('/log_in')
    def log_in():
        return 'Login'
    return app
