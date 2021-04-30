#include <BLEAdvertisedDevice.h>


void setup()
{
  Serial.begin(115200);
  
}

void loop()
{
  ble_init();
  ble_scan();
  delay(2000);
}
