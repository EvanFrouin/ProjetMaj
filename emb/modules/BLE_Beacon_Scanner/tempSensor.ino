#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME280.h"

// -----------------I2C-----------------
#define I2C_SDA 21 // SDA Connected to GPIO 14
#define I2C_SCL 22 // SCL Connected to GPIO 15
TwoWire I2CSensors = TwoWire(0);

// BME 280 (Using I2C)
Adafruit_BME280 bme;


void initBME280(){
  I2CSensors.begin(I2C_SDA, I2C_SCL, 100000);
  if (!bme.begin(0x76, &I2CSensors))
  {
    Serial.println("Couldn't Find BME280 Sensor");
    while(1);
  }
  else
  {
    Serial.println("BME280 Sensor Found");
  }

}

void printBME280(){

  Serial.print("Temperature = ");
  Serial.print(bme.readTemperature());
  Serial.print(" *C - ");


  Serial.print("Humidity = ");
  Serial.print(bme.readHumidity());
  Serial.println(" %");

  delay(1000);
  
}

float getTemp(){
  return bme.readTemperature();
}

float getHum(){
  return bme.readHumidity();
}
