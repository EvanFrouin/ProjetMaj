/****************************************************************************** 
Heart_Rate_Display over Bluetooth 
Publisher: https://www.circuitschools.com 
******************************************************************************/
#include <ArduinoJson.h>
#define LED_BUILTIN 2 //pin with LED to turn on when BT connected
 
DynamicJsonDocument doc(1024);
int buffered = 0;
 
void setup() {
  Serial.begin(9600);
  doc["name"]="ECG";
  // initialize digital pin 2 as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  // initialize the serial communication:
  startWIFI();   
  mqtt_init();
  
  Serial.println("Connection phase done"); // blank line in serial ...
  pinMode(41, INPUT); // Setup for leads off detection LO +
  pinMode(40, INPUT); // Setup for leads off detection LO -
  // initialize the serial BT communication:
  
}
 
void loop100ms() {
  if((digitalRead(40) == 1)||(digitalRead(41) == 1)){
    Serial.println('!');
  }
  else{
    // send the value of analog input 0 to serial:
    doc["data"][buffered]= analogRead(A0);
    buffered+=1;
  }
}

void loop1000ms() {
  Serial.println("loop1000");
  String output;
  serializeJson(doc, output);
  Serial.println(output);
  alert_mqtt(output);
  buffered = 0;
}

void loop()
{
  unsigned long tick  = millis();
  if (tick % 100 == 0)loop100ms(); 
  if (tick % 1000 == 20)loop1000ms(); 
  delay(1);
}
