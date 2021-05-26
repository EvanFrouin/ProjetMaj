import time
import paho.mqtt.client as paho
import re

broker="10.3.141.1"
port = 8883

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))
    print("topic =",str(message.topic))
    if(re.match(".*\/temp", str(message.topic))):
        print("It's a temp")
    elif(re.match(".*\/tag", str(message.topic))):
        print("It's a tag rssi")


client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
######Bind function to callback
client.on_message=on_message
#####

print("connecting to broker ",broker,port)
client.connect(broker,port)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe("anchor/#")#subscribe
time.sleep(2)
print("publishing ")
client.publish("anchor/rasp/test","on")#publish


while(True):
    time.sleep(4)


client.disconnect() #disconnect
client.loop_stop() #stop loop