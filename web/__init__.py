from flask import Flask, session
from flask_login import LoginManager
from datetime import timedelta
from .db import User, Patient, init_patients, get_patient_by_query
from .sockets import config_sockets

def config_app(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.config['SECRET_KEY'] = 'secret-key'

    app.config['MONGODB_SETTINGS'] = {
        'db': 'flask',
        'host': 'mongo',
        'port': 27017
    }


def config_db(app):
    from .db import db

    db.init_app(app)

    if len(Patient.objects) == 0:
        init_patients()


def config_session(app):
    @app.before_request
    def set_session_time_validity():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()


def config_routes(app):
    from web.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from web.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from web.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)


def create_app():

    app = Flask(__name__)

    config_app(app)

    config_db(app)

    config_session(app)

    config_routes(app)

    config_sockets(app)

    return app
