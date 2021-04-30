#include <Arduino.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>

#include <BLEEddystoneURL.h>
#include <BLEEddystoneTLM.h>
#include <BLEBeacon.h>


#define ENDIAN_CHANGE_U16(x) ((((x)&0xFF00) >> 8) + (((x)&0xFF) << 8))

#define BUFFER_SIZE 20


class Tag{
public:
    int rssi;
    bool alert;
    int rssi_nb = 1;
    
    BLEAddress mac = BLEAddress((uint8_t*)"\0\0\0\0\0\0");

    Tag(int _rssi,bool _alert,BLEAddress * _mac){
      this->rssi = _rssi;
      this->alert = _alert;
      this->mac = *_mac;
    }

    Tag(){
    }

    String toString(){
      String str_alert = this->alert ? "true": "false";
      String str_rssi = String(this->rssi);
      String str_mac((const __FlashStringHelper*) this->mac.toString().c_str());
      String output = "{\"mac\":\"" + str_mac + "\",\"rssi\":\"" + str_rssi + "\",\"alert\":\"" + str_alert + "\"}";
      return output;
    }
    
    int getRssiAvg(int new_rssi){
      this->rssi = (new_rssi + this->rssi * this->rssi_nb)/(this->rssi_nb+1);
      this->rssi_nb++;
    }

    void clearTag(){
      this->rssi_nb = 0;
    }
};



int tagListSize = 0;
Tag tagList[BUFFER_SIZE];


int addToTagList(BLEAdvertisedDevice advertisedDevice, uint8_t *payLoad){
  for(int i=0; i<tagListSize ; i++){
    if( advertisedDevice.getAddress().equals(tagList[i].mac) ){
      
      tagList[i].alert = payLoad[22] == 0xAA ? true: false;
      tagList[i].getRssiAvg(advertisedDevice.getRSSI());
      return i;
    }
  }
  if(tagListSize+1 == BUFFER_SIZE) return -1;

 
  tagList[tagListSize].rssi = advertisedDevice.getRSSI();
  tagList[tagListSize].mac = advertisedDevice.getAddress();
  tagList[tagListSize].alert = payLoad[22] == 0xAA ? true: false;
  tagList[tagListSize].rssi_nb = 1;
  Serial.print("Tag ajouté ");
  Serial.println(tagList[tagListSize].mac.toString().c_str());
  return ++tagListSize;
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks
{
  void onResult(BLEAdvertisedDevice advertisedDevice)
  {
    uint8_t *payLoad = advertisedDevice.getPayload();

    BLEUUID checkUrlUUID = (uint16_t)0xfeaa;

    // If uuid is recognised as Eddystone
    if (advertisedDevice.getServiceUUID().equals(checkUrlUUID))
    {
      // If the payload service correspond to our srevice.
      if (payLoad[18] == 0xF0 && payLoad[20] == 0xCA &&payLoad[21] == 0xFE)
      {
        // We add it to the list
        addToTagList(advertisedDevice, payLoad);
      }
    }
  }
};




void clearRssiAvg(){
  for(int i=0; i<tagListSize ; i++){
    tagList[i].clearTag();
  }
}

void listTags(){
  for(int i=0; i<tagListSize ; i++){
    Serial.printf("Tag-%d --- MAC: %s --- RSSI: %d --- Alert: %d\n", i, tagList[i].mac.toString().c_str(), tagList[i].rssi, tagList[i].alert );
  }
}


int scanTime = 15; //In seconds
BLEScan *pBLEScan;

void ble_init()
{
  Serial.println("Ble Init...");
  //esp_bt_controller_enable();
  btStart();
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  //pBLEScan->setInterval(100);
  //pBLEScan->setWindow(99); // less or equal setInterval value
}

// send the state of each tag to the server.
void ble_end(){
  init_wifi();
  for(int i=0; i<tagListSize ; i++){
    alert_mqtt(tagList[i].toString());
  }
  delay(500);
  stopWIFI();
  // reset the size to 
  tagListSize = 0;
}

void ble_scan()
{
  // put your main code here, to run repeatedly:
  Serial.println("Start scan!");
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  Serial.println("Scan done!");
  listTags();
  clearRssiAvg();
  pBLEScan->clearResults(); // delete results fromBLEScan buffer to release memory
  ble_end();
}
