#include <PubSubClient.h>
#include "WiFi.h"
#define TOPIC "/anchor/RFID"
IPAddress server(10, 3, 141, 1);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

void mqtt_init(){
 mqttClient.setServer(server, 1883);
}

void alert_mqtt(String content){
  mqttClient.setServer(server, 8883);
  Serial.println(content);
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect("Anchor1 Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      mqttClient.publish(TOPIC,content.c_str());
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
