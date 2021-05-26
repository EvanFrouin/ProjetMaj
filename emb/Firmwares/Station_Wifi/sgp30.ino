#include "SparkFun_SGP30_Arduino_Library.h"
#include <Wire.h>

SGP30 mySensor; //create an object of the SGP30 class

int tvoc = 0;
int co2 = 400;

//Initialize sensor
void init_sgp30(){
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


void handle_sgp30(){
  //mySensor.measureAirQuality();
  //sent_air_quality(String(mySensor.CO2,2), String(mySensor.TVOC,2));
  tvoc += random(-10, 10);
  co2 += random(-10, 10);
  if (tvoc < 0) tvoc =0;
  if (co2 < 0) co2 =0;
  sent_air_quality(String(co2), String(tvoc));
  
  
}

void printSGP30() {
  
  //First fifteen readings will be
  //CO2: 400 ppm  TVOC: 0 ppb
  //measure CO2 and TVOC levels
  mySensor.measureAirQuality();
  Serial.print("CO2: ");
  Serial.print(mySensor.CO2);
  Serial.print(" ppm\tTVOC: ");
  Serial.print(mySensor.TVOC);
  Serial.println(" ppb");

}
