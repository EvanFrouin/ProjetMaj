from flask import Flask
from flask_login import LoginManager


def create_app():
    from .db import db

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'

    app.config['MONGODB_SETTINGS'] = {
        'db': 'flask',
        'host': 'mongo',
        'port': 27017
    }

    db.init_app(app)

    from .db import User, Patient, init_patients, get_patient_by_query

    if len(Patient.objects) == 0:
        init_patients()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()

    from web.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from web.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from flask_socketio import SocketIO

    socketio = SocketIO(app)

    @socketio.on('mqtt-data')
    def forward_data(data):
        socketio.emit('web-data', data)

    @socketio.on('patient-id')
    def send_patient_data(id):
        patient = get_patient_by_query(True, pk=id)
        socketio.emit('patient-data', patient.to_json())

    return app
