#include <PubSubClient.h>
#include "WiFi.h"

#define deviceName "Anchor-1"
#define TOPIC "/anchor/Anc1"
IPAddress server(10, 3, 141, 1);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

void mqtt_init(){
 mqttClient.setServer(server, 8883);
}

void alert_mqtt(String content){
  bool sended = false;
  while(!sended){
    if (!mqttClient.connected()) {
      reconnect();
    }
    else {
      Serial.print("Pub data: ");
      
      // Once connected, publish an announcement...
      mqttClient.publish(TOPIC,content.c_str());
      Serial.println(content);
      //mqttClient.publish(TOPIC,"hello");
      sended = true;
    }
  }
}

void mqtt_stop(){
  mqttClient.disconnect();
}

void reconnect() {
  mqttClient.setServer(server, 8883);
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect("Anchor1 Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 0.5 seconds");
      // Wait 500 milliseconds before retrying
      delay(500);
    }
  }
}
