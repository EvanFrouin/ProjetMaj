#include <PubSubClient.h>
#include "WiFi.h"

uint64_t chipid = ESP.getEfuseMac(); 
uint16_t chip = (uint16_t)(chipid >> 32);

char topic_air[16];
char topic_ecg[16];
char topic_rfid[17];
char chip_c[8];

IPAddress server(10, 3, 141, 1);

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 

void mqtt_init(){
  mqttClient.setServer(server, 8883);
  snprintf(topic_air, 16, "anchor/%04X/air", chip);
  snprintf(topic_ecg, 16, "anchor/%04X/ecg", chip);
  snprintf(topic_rfid, 17, "anchor/%04X/rfid", chip);
  snprintf(chip_c, 8, "sta-%04X", chip);
}


void sent_air_quality(String co2, String tvoc){
  String content = "{\"co2\":\"" + co2 + "\",\"tvoc\":\"" + tvoc + "\"}";
  alert_mqtt(topic_air, content);
}

void send_ecg(String content){
  alert_mqtt(topic_ecg, content);
}

void send_rfid(String content){
  alert_mqtt(topic_rfid, content);
}

void alert_mqtt(char * topic, String content){
  bool sended = false;
  while(!sended){
    if (!mqttClient.connected()) {
      reconnect();
    }
    else {
      // Once connected, publish an announcement...
      mqttClient.publish(topic,content.c_str());
      Serial.print("Pub data: ");
      Serial.println(content);
      Serial.print("Topic: ");
      Serial.println(topic);
      sended = true;
      return;
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
