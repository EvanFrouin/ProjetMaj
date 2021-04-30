/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
   Changed to a beacon scanner to report iBeacon, EddystoneURL and EddystoneTLM beacons by beegee-tokyo
*/

#include <Arduino.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEEddystoneURL.h>
#include <BLEEddystoneTLM.h>
#include <BLEBeacon.h>

#define ENDIAN_CHANGE_U16(x) ((((x)&0xFF00) >> 8) + (((x)&0xFF) << 8))

#define BUFFER_SIZE 20


class Tag{
public:
    int rssi;
    bool alert;
    int rssi_nb;
    
    BLEAddress mac = BLEAddress((uint8_t*)"\0\0\0\0\0\0");

    Tag(int _rssi,bool _alert,BLEAddress * _mac){
      this->rssi = _rssi;
      this->alert = _alert;
      this->mac = *_mac;
    }

    Tag(){
    }
    
    int getRssiAvg(int new_rssi){
      this->rssi = (new_rssi + this->rssi * this->rssi_nb)/(this->rssi_nb+1);
      this->rssi_nb++;
      //Serial.printf("Tag----RSSI: %d \n", this->rssi);
    }

    void clearTag(){
      //this->rssi = 0;
      this->rssi_nb = 0;
    }
};

int tagListSize = 0;
Tag tagList[BUFFER_SIZE];


int scanTime = 15; //In seconds
BLEScan *pBLEScan;



void clearRssiAvg(){
  for(int i=0; i<tagListSize ; i++){
    tagList[i].clearTag();
  }
  //tagListSize = 0;
}

void listTags(){
  for(int i=0; i<tagListSize ; i++){
    Serial.printf("Tag-%d --- MAC: %s --- RSSI: %d --- Alert: %d\n", i, tagList[i].mac.toString().c_str(), tagList[i].rssi, tagList[i].alert );
  }
}


int addToTagList(BLEAdvertisedDevice advertisedDevice, uint8_t *payLoad){
  for(int i=0; i<tagListSize ; i++){
    if( advertisedDevice.getAddress().equals(tagList[i].mac) ){
      
      tagList[i].alert = payLoad[22] == 0xAA ? true: false;
      tagList[i].getRssiAvg(advertisedDevice.getRSSI());
      //tagList[i].rssi_nb++;
      //Serial.println("Tag maj");
      return i;
    }
  }
  if(tagListSize+1 == BUFFER_SIZE) return -1;

 
  tagList[tagListSize].rssi = advertisedDevice.getRSSI();
  tagList[tagListSize].mac = advertisedDevice.getAddress();
  tagList[tagListSize].alert = payLoad[22] == 0xAA ? true: false;
  tagList[tagListSize].rssi_nb = 1;
  Serial.print("Tag ajouté");
  Serial.println(tagList[tagListSize].mac.toString().c_str());
  return ++tagListSize;
}


class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  void onResult(BLEAdvertisedDevice advertisedDevice)
  {
    uint8_t *payLoad = advertisedDevice.getPayload();

    BLEUUID checkUrlUUID = (uint16_t)0xfeaa;

    if (advertisedDevice.getServiceUUID().equals(checkUrlUUID))
    {
      if (payLoad[18] == 0xF0 && payLoad[20] == 0xCA &&payLoad[21] == 0xFE)
      {
        // Found an interessting tag
        /*Serial.println("Found an EddystoneTLM beacon!");
        Serial.printf("Reported state: 0x%x%x\n", payLoad[26],payLoad[27]);
        Serial.print("RSSI: ");
        Serial.println(advertisedDevice.getRSSI());
        Serial.print("MAC: ");
        Serial.println(advertisedDevice.getAddress().toString().c_str());
        Serial.println("");*/
        addToTagList(advertisedDevice, payLoad);
        if (payLoad[22] == 0xAA && payLoad[23] == 0xAA){
          Serial.println("FULL ALERTE");
        }
      }
    }
  }
};

void setup()
{
  Serial.begin(115200);
  Serial.println("Scanning...");

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99); // less or equal setInterval value
}

void loop()
{
  // put your main code here, to run repeatedly:
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  Serial.println("Scan done!");
  listTags();
  clearRssiAvg();
  pBLEScan->clearResults(); // delete results fromBLEScan buffer to release memory
  delay(2000);
}
