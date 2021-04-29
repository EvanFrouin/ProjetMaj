#include "SparkFun_SGP30_Arduino_Library.h"
#include <Wire.h>

SGP30 mySensor; //create an object of the SGP30 class

void setup() {
  Serial.begin(9600);
  initSGP30();
  
}

void loop() {
 printSGP30();
}

//Initialize sensor
void initSGP30(){
  Wire.begin();
  if (mySensor.begin() == false) {
    Serial.println("No SGP30 Detected. Check connections.");
    while (1);
  }
  //Initializes sensor for air quality readings
  //measureAirQuality should be called in one second increments after a call to initAirQuality
  mySensor.initAirQuality();
}

int getCO2(){
  mySensor.measureAirQuality();
  return mySensor.CO2;
}

int getTVOC(){
  mySensor.measureAirQuality();
  return mySensor.TVOC;
}

SGP30 getSGP30(){
  return mySensor;
}


void printSGP30() {
  //First fifteen readings will be
  //CO2: 400 ppm  TVOC: 0 ppb
  delay(1000); //Wait 1 second
  //measure CO2 and TVOC levels
  mySensor.measureAirQuality();
  Serial.print("CO2: ");
  Serial.print(mySensor.CO2);
  Serial.print(" ppm\tTVOC: ");
  Serial.print(mySensor.TVOC);
  Serial.println(" ppb");

}

