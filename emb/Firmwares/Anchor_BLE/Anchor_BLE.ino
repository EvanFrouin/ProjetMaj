#include <BLEAdvertisedDevice.h>


void setup()
{
  initBME280();
  mqtt_init();
  Serial.begin(115200);
  
}

void loop()
{
  ble_scan();
  delay(2000);
}
