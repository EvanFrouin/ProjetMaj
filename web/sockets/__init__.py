import json
from mongoengine import OperationError

from ..db import *


def config_sockets(app):
    from flask_socketio import SocketIO

    socketio = SocketIO(app)

    @socketio.on('mqtt-data')
    def forward_data(data):
        
        data = json.loads(data)
        socket_name = "SOCKET_" + data["publisher"] + "_" + data["datatype"]
        
        if(data["datatype"] == "temp" ):
            socketio.emit(socket_name, data["temp"])
        elif(data["datatype"] == "hum" ):
            socketio.emit(socket_name, data["hum"])
        elif(data["datatype"] == "voc" ):
            socketio.emit(socket_name, data["tvoc"])
        elif(data["datatype"] == "co2" ):
            socketio.emit(socket_name, data["co2"])
        elif(data["datatype"] == "ecg" ):
            response  = {"ecg_pot":data["ecg_pot"], "reading_number": data["reading_number"]}
            socketio.emit(socket_name, json.dumps(response))
        elif(data["datatype"] == "rfid" ):
            socketio.emit(socket_name, data["uid"])
        elif(data["datatype"] == "pos" ):
            #socketio.emit(socket_name, data["mac"])
            patient_id = get_patient_id_from_mac(data["mac"])
            tag_name = get_tag_name(data["mac"])+ " - " +get_patient_name_from_mac(patient_id)
            response  = {"mac":data["mac"], "patient_name": tag_name, "id":patient_id }
            socketio.emit(socket_name, json.dumps(response))
        elif(data["datatype"] == "alert" ):
            socketio.emit(socket_name, data["mac"])




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
            print("Can't modify patient")
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
