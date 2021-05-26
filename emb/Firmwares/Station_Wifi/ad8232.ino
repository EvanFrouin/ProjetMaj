#include <ArduinoJson.h>
 
DynamicJsonDocument doc(4096);
int buffer_size = 0;


void init_ad8232(){
  pinMode(41, INPUT); // Setup for leads off detection LO +
  pinMode(40, INPUT); // Setup for leads off detection LO -
}


void read_ad8232(){
  if((digitalRead(40) == 1)||(digitalRead(41) == 1)){
    Serial.println('!');
  }
  else{
    // send the value of analog input 0 to serial:
    doc["ecg_pot"][buffer_size]= analogRead(A0);
    buffer_size+=1;
  }
  if(buffer_size ==10){
    handle_ad8232();
  }
}


void handle_ad8232(){
  doc["reading_number"] = buffer_size;
  buffer_size = 0;
  
  String output;
  serializeJson(doc, output);
  //Serial.println(output);
  send_ecg(output);
}
