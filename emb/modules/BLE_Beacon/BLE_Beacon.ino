/*
   EddystoneTLM beacon by BeeGee based on https://github.com/pcbreflux/espressif/blob/master/esp32/arduino/sketchbook/ESP32_Eddystone_TLM_deepsleep/ESP32_Eddystone_TLM_deepsleep.ino
   EddystoneTLM frame specification https://github.com/google/eddystone/blob/master/eddystone-tlm/tlm-plain.md
*/

/*
   Create a BLE server that will send periodic Eddystone URL frames.
   The design of creating the BLE server is:
   1. Create a BLE Server
   2. Create advertising data
   3. Start advertising.
   4. wait
   5. Stop advertising.
   6. deep sleep
   
*/
#include "sys/time.h"

#include <Arduino.h>

#include "BLEDevice.h"
#include "BLEUtils.h"
#include "BLEBeacon.h"
#include "BLEAdvertising.h"
#include "BLEEddystoneURL.h"

#include "esp_sleep.h"

#define GPIO_DEEP_SLEEP_DURATION 10     // sleep x seconds and then wake up
RTC_DATA_ATTR static time_t last;    // remember last boot in RTC Memory
RTC_DATA_ATTR static uint32_t bootcount; // remember number of boots in RTC Memory

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
BLEAdvertising *pAdvertising;
struct timeval nowTimeStruct;

time_t lastTenth;

bool alert = false;
uint16_t uChipId = ESP.getEfuseMac();
String DeviceName = "Tag32-" + String(uChipId, HEX);

#define BEACON_UUID "8ec76ea3-6668-48da-9866-75be8bc86f4d" // UUID 1 128-Bit (may use linux tool uuidgen or random numbers via https://www.uuidgenerator.net/)


void setBeacon()
{
  char beacon_data[25];
  uint16_t beconUUID = 0xFEAA;
  uint16_t serviceID = 0xCAFE;
  uint16_t stateCode = 0; 
  if(alert)stateCode = 0xAAAA;
  Serial.printf("State Code %0X%0X\n", (stateCode >> 8), (stateCode & 0xFF));

  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();
  BLEAdvertisementData oScanResponseData = BLEAdvertisementData();

  oScanResponseData.setFlags(0x06); // GENERAL_DISC_MODE 0x02 | BR_EDR_NOT_SUPPORTED 0x04
  oScanResponseData.setCompleteServices(BLEUUID(beconUUID));

  beacon_data[0] = 0xF0;                // Positionning Endpoint (diy for us)
  beacon_data[1] = 0x00;                // TLM version TODO : change for non-debug
  beacon_data[2] = (serviceID >> 8);           // Battery voltage, 1 mV/bit i.e. 0xCE4 = 3300mV = 3.3V
  beacon_data[3] = (serviceID & 0xFF);           //
  beacon_data[4] = (stateCode >> 8);           // Beacon temperature
  beacon_data[5] = (stateCode & 0xFF);           //
  beacon_data[6] = ((bootcount & 0xFF000000) >> 24);  // Advertising PDU count
  beacon_data[7] = ((bootcount & 0xFF0000) >> 16);  //
  beacon_data[8] = ((bootcount & 0xFF00) >> 8);   //
  beacon_data[9] = (bootcount & 0xFF);        //
  beacon_data[10] = ((lastTenth & 0xFF000000) >> 24); // Time since power-on or reboot as 0.1 second resolution counter
  beacon_data[11] = ((lastTenth & 0xFF0000) >> 16);   //
  beacon_data[12] = ((lastTenth & 0xFF00) >> 8);    //
  beacon_data[13] = (lastTenth & 0xFF);       //

  oScanResponseData.setServiceData(BLEUUID(beconUUID), std::string(beacon_data, 14));
  oAdvertisementData.setName("Tag32");
  pAdvertising->setAdvertisementData(oAdvertisementData);
  pAdvertising->setScanResponseData(oScanResponseData);
}

void setup()
{

  Serial.begin(115200);
  gettimeofday(&nowTimeStruct, NULL);

  Serial.printf("start ESP32 %d\n", bootcount++);

  Serial.printf("deep sleep (%lds since last reset, %lds since last boot)\n", nowTimeStruct.tv_sec, nowTimeStruct.tv_sec - last);


  //Print the wakeup reason for ESP32
  alert = userReboot();
  if(alert){
    Serial.printf("user ALERT");
  }

  last = nowTimeStruct.tv_sec;
  lastTenth = nowTimeStruct.tv_sec * 10; // Time since last reset as 0.1 second resolution counter

  // Create the BLE Device
  BLEDevice::init("TLMBeacon");

  BLEDevice::setPower(ESP_PWR_LVL_N12);

  pAdvertising = BLEDevice::getAdvertising();

  setBeacon();
  // Start advertising
  pAdvertising->start();
  Serial.println("Advertizing started for 10s ...");
  delay(10000);
  pAdvertising->stop();
  Serial.printf("enter deep sleep for 10s\n");
  esp_deep_sleep(1000000LL * GPIO_DEEP_SLEEP_DURATION);
  Serial.printf("in deep sleep\n");
}

void loop()
{
}


bool userReboot(){
  esp_sleep_wakeup_cause_t wakeup_reason;
  wakeup_reason = esp_sleep_get_wakeup_cause();
  switch(wakeup_reason)
  {
    case 1  : 
    case 2  : 
    case 3  : 
    case 4  : 
    case 5  : return false; break;
    default : return true; break;
  }
}
