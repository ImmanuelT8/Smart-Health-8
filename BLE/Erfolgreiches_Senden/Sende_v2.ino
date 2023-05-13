/*
    Video: https://www.youtube.com/watch?v=oCMOYS71NIU
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
    Ported to Arduino ESP32 by Evandro Copercini
    updated by chegewara

   Create a BLE server that, once we receive a connection, will send periodic notifications.
   The service advertises itself as: 4fafc201-1fb5-459e-8fcc-c5c9c331914b
   And has a characteristic of: beb5483e-36e1-4688-b7f5-ea07361b26a8

   The design of creating the BLE server is:
   1. Create a BLE Server
   2. Create a BLE Service
   3. Create a BLE Characteristic on the Service
   4. Create a BLE Descriptor on the characteristic
   5. Start the service.
   6. Start advertising.

   A connect hander associated with the server starts a background task that performs notification
   every couple of seconds.
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

int Parameter[4];

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
std::string value = "0";
std::string ledbrightness = "50";
std::string sample_avg = "SAMPLEAVG_4";
std::string mode2 = "MODE_MULTILED";
std::string sample_rate = "SAMPLERATE_100";
std::string pulse_width = "PULSEWIDTH_411";
std::string adc_range = "ADCRANGE_16384";

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};


// Diese Funktion zerlegt einen String in Teilstrings anhand eines Trennzeichens
std::vector<std::string> splitString(std::string s, std::string delimiter) {   // Initialisiere ein Vektor-Objekt, das die Teilstrings enthält
  std::vector<std::string> result;                                    // Initialisiere eine Variable, um den Anfang des nächsten Teilstrings zu speichern
  size_t pos = 0;                                                   // Initialisiere eine Variable für den aktuellen Teilstring
  std::string token;                                              // Suche nach dem Trennzeichnen im String und extrahiere die Teilstrings
  while ((pos = s.find(delimiter)) != std::string::npos) {      // Extrahiere den Teilstring bis zum Trennzeichnen
    token = s.substr(0, pos);                                 // Füge den Teilstring zum Vektor hinzu
    result.push_back(token);                                  // Entferne den extrahierten Teilstring aus dem String
    s.erase(0, pos + delimiter.length());
  }
  // Füge den verbleibenden Rest des Strings als letzten Teilstring hinzu
  result.push_back(s);
  // Gib den Vektor mit den Teilstrings zurück
  return result;
}



class MyCallbacks : public BLECharacteristicCallbacks {  // Diese Funktion wird aufgerufen, wenn ein Wert auf dem Charakteristikum geschrieben wird
    void onWrite(BLECharacteristic *pCharacteristic) {     // Lese den Wert, der geschrieben wurde, aus dem Charakteristikum aus
      std::string value = pCharacteristic->getValue();                   // Zerlege den String in Teilstrings, die durch Leerzeichen getrennt sind
      std::vector<std::string> parameters = splitString(value, " ");      // Gehe durch jeden Teilstring und gib ihn aus
      for (int i = 0; i < parameters.size(); i++) {                        // Gib den Index des Parameters und seinen Wert aus
        Serial.print("Received parameter ");
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.println(parameters[i].c_str());

        if (i == 0)
        {
          ledbrightness = parameters[i].c_str();
        }

        if (i == 1)
        {
          sample_avg = parameters[i].c_str();
        }

        if (i == 2)
        {
          mode2 = parameters[i].c_str();
        }

        if (i == 3)
        {
          sample_rate = parameters[i].c_str();
        }

        if (i == 4)
        {
          pulse_width = parameters[i].c_str();
        }

        if (i == 5)
        {
          adc_range = parameters[i].c_str();
        }

        std::string received_message = "Werte empfangen!";
        pCharacteristic->setValue(received_message);
        pCharacteristic->notify();


      }
    }
};




void setup() {
  Serial.begin(115200);

  // Create the BLE Device
  BLEDevice::init("ESP32");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );

  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");


  pCharacteristic->setCallbacks(new MyCallbacks());

}

void loop() {
  // notify changed value
  if (deviceConnected) {

  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }

}
