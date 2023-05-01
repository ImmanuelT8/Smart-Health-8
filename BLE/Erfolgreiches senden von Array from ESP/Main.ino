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

#include <DFRobot_MAX30102.h>
DFRobot_MAX30102 particleSensor;

int Wert;

// Datenarray zum Senden von Daten über das BLE-Charakteristikum
int data[100] = {0};  // 100 Integer-Werte, initialisiert mit 0


BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value;

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



void setup() {
  Serial.begin(115200);

  // Sensor initialisieren
  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }

  // Sensor konfigurieren
  particleSensor.sensorConfiguration(/*ledBrightness=*/50, /*sampleAverage=*/SAMPLEAVG_4, \
      /*ledMode=*/MODE_MULTILED, /*sampleRate=*/SAMPLERATE_100, \
      /*pulseWidth=*/PULSEWIDTH_411, /*adcRange=*/ADCRANGE_16384);

  // Create the BLE Device
  BLEDevice::init("ESP_SPO2");

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
}


int32_t SPO2; //SPO2
int8_t SPO2Valid; //Flag to display if SPO2 calculation is valid
int32_t heartRate; //Heart-rate
int8_t heartRateValid; //Flag to display if heart-rate calculation is valid
int red;




void loop() {

  // Zuerst Daten im Array sammeln

  // Sammle Daten, Verschiebe alle Elemente im Array um eins nach rechts


  if (Wert <= 99) {

    Serial.println(Wert);

    // Füge den neuen Wert am Index 0 hinzu
    data[Wert] = particleSensor.getRed();

    Wert = Wert + 1;



  }



  else {

    // Reset meines Parameters Wert
    Wert = 0;

    // Array voll
    Serial.println("100 Werte im Array gesammelt");

    Serial.println("Bin in vor Schleife Gerät Verbunden");

    // Ausgabe der gesammelten Daten
    Serial.println(); // Neue Zeile am Ende der Ausgabe

    Serial.print("ESP verbunden, sende Daten");

    Serial.println(); // Neue Zeile am Ende der Ausgabe
    pCharacteristic->setValue((uint8_t*)data, sizeof(data));

    pCharacteristic->notify();
    Serial.println("Verbunden im Loop");

    //  memset(data, 0, sizeof(data));

    // Zurücksetzen der Variablen für die nächste Datensammlung




    if (!deviceConnected) {

      // Serial Print das Array wenn nicht verbunden

      Serial.println("ESP nicht verbunden. Daten: ");

      for (int i = 0; i < 100; i++) { // Durchlaufen des Arrays
        Serial.print(data[i]); // Ausgabe des aktuellen Elements
        Serial.print(" "); // Trennzeichen zwischen den Elementen
        Serial.println(); // Neue Zeile am Ende der Ausgabe

      }
    }

  }


  if (!deviceConnected) {


    if (Wert >= 99)

    {

      // Reset meines Parameters Wert
      Wert = 0;

      // Wenn nicht verbunden BLE bewerben

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
  }
}

