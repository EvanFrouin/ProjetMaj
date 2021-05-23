import json
from mongoengine import OperationError

from ..db import *


def config_sockets(app):
    from flask_socketio import SocketIO

    socketio = SocketIO(app)

    @socketio.on('mqtt-data')
    def forward_data(data):
        socketio.emit('web-data', data)

    @socketio.on('patient-data-q')
    def patient_data(patient_id):
        patient = get_patient_by_query(True, pk=patient_id)
        socketio.emit('patient-data-r', patient.to_json())

    @socketio.on('patient-reset-q')
    def patients_reset():
        try:
            reset_patient_collection()
            code = 0
        except:
            code = 1
        finally:
            socketio.emit('patient-reset-r', code)

    @socketio.on('patient-delete-q')
    def patient_delete(patient_id):
        try:
            delete_patient(patient_id)
            code = 0
        except:
            code = 1
        finally:
            socketio.emit('patient-delete-r', (patient_id, code))

    @socketio.on('patient-update-q')
    def patient_update(data):
        try:
            data_dict = json.loads(data)
            patient_id = data_dict.pop("id")
            update_patient(patient_id, data_dict)
            code = 0
        except:
            code = 1
        finally:
            socketio.emit('patient-update-r', code)

    @socketio.on('user-role-q')
    def user_delete(user_id):
        try:
            delete_user(user_id)
            code = 0
        except OperationError:
            code = 1
        finally:
            socketio.emit('user-delete-r', (user_id, code))

    @socketio.on('user-role-q')
    def user_role(user_id):
        try:
            update_user_role(user_id)
            code = 0
        except:
            code = 1
        finally:
            socketio.emit('user-role-r', code)
