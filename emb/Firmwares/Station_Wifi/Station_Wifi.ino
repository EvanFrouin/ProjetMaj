void setup() {
  // put your setup code here, to run once
  randomSeed(analogRead(1));
  Serial.begin(115200);
  init_wifi();
  mqtt_init();
  //init_sgp30();
  init_ad8232();
  init_rc522();
}


void loop20ms(){
  
}


void loop250ms(){
  read_ad8232();
  handle_rc522();
  
}

void loop1000ms(){
  Serial.println("loop 1sec");
  //handle_ad8232();
  //handle_sgp30();
}

void loop20s(){
  handle_sgp30();
}

void loop()
{
  unsigned long tick  = millis();
  if (tick % 20 == 0)loop20ms(); 
  if (tick % 250 == 0)loop250ms(); 
  if (tick % 1000 == 0)loop1000ms(); 
  if (tick % 20000 == 0)loop20s(); 
  if (tick == millis())delay(1); 
  
  
}
