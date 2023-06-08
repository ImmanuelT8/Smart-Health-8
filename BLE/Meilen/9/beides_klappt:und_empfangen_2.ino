#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <DFRobot_MAX30102.h>
DFRobot_MAX30102 particleSensor;

int Wert; // Variable die bei jedem Erfassen der Daten erhöht wird um dann bei 100 Werten das Array abzuschließen und das Senden einzuleiten

// Datenarray zum Senden von Daten über das BLE-Charakteristikum
int data[100] = {0};  // 100 Integer-Werte, initialisiert mit 0
int dataIR[100] = {0};  // 100 Integer-Werte, initialisiert mit 0

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
BLECharacteristic* pCharacteristic2 = NULL;
BLECharacteristic* pCharacteristic3 = NULL;

uint32_t ledBrightness1 = 50;
uint8_t sampleAverage1 = SAMPLEAVG_4;
uint8_t ledMode1 = MODE_MULTILED;
int16_t sampleRate1 = SAMPLERATE_100;
uint16_t pulseWidth1 = PULSEWIDTH_411;
uint16_t adcRange1 = ADCRANGE_16384;
bool deviceConnected = false;
bool updateSensor = false;
//uint32_t value;

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
#define CHARACTERISTIC_UUID2 "beb5483e-36e1-4688-b7f5-ea07361b26a9"
#define CHARACTERISTIC_UUID3 "5a464637-3fe1-4685-9e33-ec4ba175f081"


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
};



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




void updateSensorConfig() {
  // Sensor konfigurieren
  particleSensor.sensorConfiguration(ledBrightness1, sampleAverage1, ledMode1, sampleRate1, pulseWidth1, adcRange1);
  Serial.println("Sensor configuration updated");
}



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

  pCharacteristic2 = pService->createCharacteristic(
                       CHARACTERISTIC_UUID2,
                       BLECharacteristic::PROPERTY_READ   |
                       BLECharacteristic::PROPERTY_WRITE  |
                       BLECharacteristic::PROPERTY_NOTIFY |
                       BLECharacteristic::PROPERTY_INDICATE
                     );

  // Charakteristik für Update

  pCharacteristic3 = pService->createCharacteristic(
                       CHARACTERISTIC_UUID3,
                       BLECharacteristic::PROPERTY_READ   |
                       BLECharacteristic::PROPERTY_WRITE  |
                       BLECharacteristic::PROPERTY_NOTIFY |
                       BLECharacteristic::PROPERTY_INDICATE
                     );

  
  // Initialisiere den Callback für das dritte Charakteristikum zum Empfangen der Parameter
  pCharacteristic3->setCallbacks(new MyCallbacks());

  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLE2902());
  pCharacteristic2->addDescriptor(new BLE2902());
  pCharacteristic3->addDescriptor(new BLE2902());

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
int IR;


void loop() {

  // Zuerst Daten im Array sammeln
  // Sammle Daten, Verschiebe alle Elemente im Array um eins nach rechts


  if (Wert <= 99) {

    Serial.println(Wert);

    // Füge den neuen Wert am Index 0 hinzu
    data[Wert] = particleSensor.getRed();
    dataIR[Wert] = particleSensor.getIR();
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

    Serial.println(); // Neue Zeile am Ende der Ausgabe
    pCharacteristic->setValue((uint8_t*)data, sizeof(data));
    pCharacteristic2->setValue((uint8_t*)dataIR, sizeof(dataIR));

    pCharacteristic->notify();
    pCharacteristic2->notify();

    Serial.println("Sende Daten:");


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

    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");

  }

    if (updateSensor) {
    updateSensorConfig();
    updateSensor = false;
  }

}
