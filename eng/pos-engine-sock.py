import time
import paho.mqtt.client as paho
import re
import json

from pymongo import MongoClient
import urllib.parse
import ast

import requests
import socketio
import random
import time
import signal
import sys

from datetime import datetime

# Todo : add the socket to push data to the webserver.
# https://realpython.com/python-sockets/



broker="10.3.141.1"
port = 8883

mongo_login = "root"
mongo_pass = "example"

temp_col = None
rssi_col = None
pos_col = None

############################## Begin global Socket 
def signal_handler(sig, frame):
    print("\rExiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

soc = socketio.Client()
soc.sleep(1)
soc.connect("http://10.3.141.1:5000")


def send_to_socket(data):
    print("Data sent: ", data)
    try:
        soc.emit("mqtt-data", data)
    except:
        soc.connect("http://10.3.141.1:5000")
        print("couldn't send the data to socket")
############################## End global Socket 


def get_pub_id(str):
    anc = re.sub(r"[a-z]+\/", "", str)
    return re.sub(r"\/[a-z]+", "", anc)


tags = []
def process_pos(content):
    global tags
    
    ble_position = {'mac':content['mac'],'publisher':content['publisher'],'rssi':content['rssi'],'date': content['date']}

    found_tag = False
    for t in tags:
        # Find the tag 
        if t['mac'] == content['mac']:
            found_tag = True
            found_pub = False 
            t['position']['rssi'] = "-100"
            t['position']['date'] = content['date']
            for p in t['publishers']:
                p['notSeen'] += 1
                # Find the anchor (publisher)
                if p['publisher'] == content['publisher']:
                    found_pub = True
                    p['notSeen'] = 0
                    p['rssi'] = content['rssi']


                # Find the anchor (publisher) with the biggest rssi
                if int(p['rssi']) > int(t['position']['rssi']) and p['notSeen'] < 10:
                    t['position']['rssi'] = p['rssi']
                    t['position']['publisher'] = p['publisher']

            if not found_pub:
                pub = {'publisher':content['publisher'],'rssi':content['rssi'],'notSeen':0}
                t['publishers'].append(pub)

            #Save the position
            ble_position = t['position']
            #pos_col.insert_one(ble_position)
    
    if not found_tag:
        tag = {'mac':content['mac'],'publishers':[{'publisher':content['publisher'],'rssi':content['rssi'],'notSeen':0}],'position':ble_position}
        tags.append(tag)

    ble_position['date'] = content['date']
    #pos_col.insert_one(ble_position.copy())

    #print("## TAGS ##")
    #print(tags)
    #print("## POSITION ##")
    #print(ble_position)
    return ble_position.copy()

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    #print("topic =",str(message.topic))

    try:
        content = ast.literal_eval(message.payload.decode("utf-8").replace('"', "'"))
        anchor = get_pub_id(str(message.topic))
    except:
        print("not able to decode content ")
        return
    
    # Format the data for later 
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")



    content.update({'publisher':anchor,'date':date_time}) # Add the publisher and date to the value

    # content: {"temp":"24","hum":"5", 'publisher': '88FA', 'date': '05/06/2021, 20:58:34'}  topic : anchor/IDXX/temp
    if(re.match(".*\/temp", str(message.topic))):
        #print(content)
        
        #temp_col.insert_one(content) # Save the data in the database
        content.update({'datatype':'temp'}) # Add the datatype value for websocket
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json 
        content.update({'datatype':'hum'}) # Add the datatype value for websocket
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json 
    
    # content: {'mac': 'ac:67:b2:38:77:1a', 'rssi': '-18', "alert":0, 'publisher': '88FA', 'date': '05/06/2021, 20:58:34'}";  topic : anchor/IDXX/tag
    elif(re.match(".*\/tag", str(message.topic))):
        #print(content)
        #rssi_col.insert_one(content)# Save the rssi in the database

        new_content = process_pos(content)# Add the position data to DB and return the position. 
        new_content.update({'datatype':'pos'})
        send_to_socket(json.dumps(new_content))#Send the data to the client formatted in str json 

        if(content['alert'] == 'true'):
            print("ALERT OMG")
            content.update({'datatype':'alert'})
            send_to_socket(json.dumps(content))

    # content: {"values":[49,65,64,267,3763,36,37,36,37,37], 'publisher': '88FA', 'date': '05/06/2021, 20:58:34'}  topic : anchor/IDXX/ecg
    elif(re.match(".*\/ecg", str(message.topic))):
        #ecg_col.insert_one(content)# Save the rssi in the database

        content.update({'datatype':'ecg'})# Add the datatype to the json
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json 

    elif(re.match(".*\/air", str(message.topic))):
        #ecg_col.insert_one(content)# Save the rssi in the database

        content.update({'datatype':'voc'})# Add the datatype to the json
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json
        content.update({'datatype':'co2'})# Add the datatype to the json
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json

    elif(re.match(".*\/rfid", str(message.topic))):
        #ecg_col.insert_one(content)# Save the rssi in the database

        content.update({'datatype':'rfid'})# Add the datatype to the json
        send_to_socket(json.dumps(content))#Send the data to the client formatted in str json


def main():
    # establing connection to db
    try:
        #connect = MongoClient("10.3.141.1" ,27017)
        #connect.sensors.authenticate(mongo_login, mongo_pass)
        #connect = MongoClient('mongodb://' + mongo_login + ':' + mongo_pass + '@127.0.0.1:27017')
        connect = MongoClient('10.3.141.1:27017')
        connect.authenticate(mongo_login, mongo_pass)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
        
    # connecting or switching to the databases
    """
    sensorDB = connect.sensors

    # creating or switching to demoCollection
    global temp_col
    global rssi_col
    global pos_col
    global ecg_col
    temp_col = sensorDB.temp
    rssi_col = sensorDB.rssi
    pos_col = sensorDB.positionning
    ecg_col = sensorDB.ecg

    """
    client= paho.Client("client-001") 
    ######Bind function to callback
    client.on_message=on_message
    #####

    print("connecting to broker ",broker,port)
    client.connect(broker,port)#connect
    client.loop_start() #start loop to process received messages
    print("subscribing ")
    client.subscribe("anchor/#")#subscribe

    

    

    # We loop waiting for callbacks
    while(True):
        time.sleep(4)

if __name__ == "__main__":
    # execute only if run as a script
    main()