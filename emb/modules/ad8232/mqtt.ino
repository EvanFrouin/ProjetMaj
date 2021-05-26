#include <PubSubClient.h>
#include "WiFi.h"
#define TOPIC "anchor/ECG"
IPAddress server(10, 3, 141, 1);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

void mqtt_init(){
 mqttClient.setServer(server, 8883);
 if(mqttClient.connect("mqtt")){
   Serial.println("MQTT Broker connected");
 }
 else{
   Serial.println("Error MQTT Broker connection");
 }
}

void alert_mqtt(String content){
  if (mqttClient.connected()) 
    {
      mqttClient.publish(TOPIC,content.c_str());
    } 
    else {
      reconnect();
    }
}

void reconnect() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect("Anchor1 Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      mqttClient.publish("/anchor/Anc1","hello world");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
  mqttClient.disconnect();
}
