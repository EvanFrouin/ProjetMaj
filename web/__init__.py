from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

db = MongoEngine()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'

    app.config['MONGODB_SETTINGS'] = {
        'db': 'flask',
        'host': 'localhost',
        'port': 27017
    }

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
