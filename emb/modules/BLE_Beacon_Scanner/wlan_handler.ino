#include "WiFi.h"
#include <ESPmDNS.h>

//WiFi Connection configuration
const char *ssid = "IoT_Defi";
const char *password = "getoutofmylan";

void init_wifi(){
  if(WiFi.status() != WL_CONNECTED) {
    startWIFI();
  }
}

void stopWIFI() {
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
}

void startWIFI() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("MAC address: ");
  Serial.println(WiFi.macAddress());
  
}
