import time
import paho.mqtt.client as paho
import re

from pymongo import MongoClient
import urllib.parse
import ast

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

def getPubId(str):
    anc = re.sub(r"[a-z]+\/", "", str)
    return re.sub(r"\/[a-z]+", "", anc)


tags = []
def processPos(content):
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
    pos_col.insert_one(ble_position.copy())

    #print("## TAGS ##")
    #print(tags)
    print("## POSITION ##")
    print(ble_position)

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    #print("topic =",str(message.topic))

    try:
        content = ast.literal_eval(message.payload.decode("utf-8").replace('"', "'"))
    except:
        print("not able to decode content ")
        return
    
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if(re.match(".*\/temp", str(message.topic))):
        anchor = getPubId(str(message.topic))
        content.update({'publisher':anchor,'date':date_time})
        
        #print(content)
        temp_col.insert_one(content)
        #print("received message =",str(message.payload.decode("utf-8")))
        
    elif(re.match(".*\/tag", str(message.topic))):
        anchor = getPubId(str(message.topic))
        content.update({'publisher':anchor,'date':date_time})
        
        #print(content)
        rssi_col.insert_one(content)
        processPos(content)
        #print("received message =",str(message.payload.decode("utf-8")))


def main():
    client= paho.Client("client-001") 
    ######Bind function to callback
    client.on_message=on_message
    #####

    print("connecting to broker ",broker,port)
    client.connect(broker,port)#connect
    client.loop_start() #start loop to process received messages
    print("subscribing ")
    client.subscribe("anchor/#")#subscribe

    # establing connection to db
    try:
        connect = MongoClient('localhost:27017')
        connect.sensors.authenticate(mongo_login, mongo_pass)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the databases

    sensorDB = connect.sensors

    # creating or switching to demoCollection
    global temp_col
    global rssi_col
    global pos_col
    temp_col = sensorDB.temp
    rssi_col = sensorDB.rssi
    pos_col = sensorDB.positionning

    while(True):
        time.sleep(4)

if __name__ == "__main__":
    # execute only if run as a script
    main()