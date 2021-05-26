#include <PubSubClient.h>
#include "WiFi.h"

uint64_t chipid = ESP.getEfuseMac(); 
uint16_t chip = (uint16_t)(chipid >> 32);
char topic_tag[16];
char topic_temp[17];
char chip_c[8];

IPAddress server(10, 3, 141, 1);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

void mqtt_init(){
  mqttClient.setServer(server, 8883);
  snprintf(topic_tag, 16, "anchor/%04X/tag", chip);
  snprintf(topic_temp, 17, "anchor/%04X/temp", chip);
  snprintf(chip_c, 8, "anc-%04X", chip);
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
      mqttClient.publish(topic_tag,content.c_str());
      Serial.println(content);
      sended = true;
    }
  }
}

void temp_mqtt(){
  bool sended = false;
  while(!sended){
    if (!mqttClient.connected()) {
      reconnect();
    }
    else {

      Serial.print("Pub temp: ");
      String content = "{\"temp\":\"" + String(getTemp(),2) + "\",\"hum\":\"" + String(getHum(),2) + "\"}";
      // Once connected, publish an announcement...
      mqttClient.publish(topic_temp,content.c_str());
      Serial.println(content);
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
    if (mqttClient.connect(chip_c)) {
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
