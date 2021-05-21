from ..db import get_patient_by_query

def config_sockets(app):
    from flask_socketio import SocketIO

    socketio = SocketIO(app)

    @socketio.on('mqtt-data')
    def forward_data(data):
        socketio.emit('web-data', data)

    @socketio.on('patient-id')
    def send_patient_data(id):
        patient = get_patient_by_query(True, pk=id)
        socketio.emit('patient-data', patient.to_json())

