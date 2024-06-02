#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <DFRobot_MAX30102.h>
#include <string> // Header für std::stoi und std::stoul
#include <stdlib.h>
 
 
DFRobot_MAX30102 particleSensor;
 
int Wert; // Variable die bei jedem Erfassen der Daten erhöht wird um dann bei 100 Werten das Array abzuschließen und das Senden einzuleiten
 
// Datenarray zum Senden von Daten über das BLE-Charakteristikum
int data[100] = {0};  // 100 Integer-Werte, initialisiert mit 0
int dataIR[100] = {0};  // 100 Integer-Werte, initialisiert mit 0
 
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
BLECharacteristic* pCharacteristic2 = NULL;
BLECharacteristic* pCharacteristic3 = NULL;

int LED_BUILTIN = 2;
int LED_off_on; 
int ledBrightness1 = 50;
 
int sampleAverage1 = 50; ;
int ledMode1 = 50; ;
int sampleRate1 = 50; ;
int pulseWidth1 = 50; ;
int adcRange1 = 50; ;
 
bool deviceConnected = false;
bool updateSensor = false;
 
// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
 
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHARACTERISTIC_UUID2 "beb5483e-36e1-4688-b7f5-ea07361b26a9"
#define CHARACTERISTIC_UUID3 "5a464637-3fe1-4685-9e33-ec4ba175f081"
 
 
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      digitalWrite(LED_BUILTIN, HIGH);
    };
 
    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};
 
// Diese Funktion zerlegt einen String in Teilstrings anhand eines Trennzeichens
std::vector<std::string> splitString(std::string s, std::string delimiter) {
  std::vector<std::string> result;
  size_t pos = 0;
  std::string token;
  while ((pos = s.find(delimiter)) != std::string::npos) {
    token = s.substr(0, pos);
    result.push_back(token);
    s.erase(0, pos + delimiter.length());
  }
  result.push_back(s);
  return result;
}


 class MyCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();
    std::vector<std::string> parameters = splitString(value, ",");
    
    if (parameters.size() == 6) {
      
      //ledBrightness1 = parameters[0];
      ledBrightness1 = atoi(parameters[0].c_str());

      //sampleAverage1 = parameters[1];
      sampleAverage1 = atoi(parameters[1].c_str());
      
      //ledMode1 = parameters[2];
      ledMode1 = atoi(parameters[2].c_str());
      
      //sampleRate1 = parameters[3];
      sampleRate1 = atoi(parameters[3].c_str());
      
      //pulseWidth1 = parameters[4];
      pulseWidth1 = atoi(parameters[4].c_str()); 
      
      //adcRange1 = parameters[5];
      adcRange1 = atoi(parameters[5].c_str());
      
        Serial.print("Led Helligkeit = ");
        Serial.print(ledBrightness1);
        //Serial.print(ledBrightness1);
        Serial.print("; ");
        Serial.print("Durchschnitt  = ");
        Serial.print(sampleAverage1);
        //Serial.print(sampleAverage1);
        Serial.print("; ");
        Serial.print("Led Modus  = ");
        Serial.print(ledMode1);
        //Serial.print(ledMode1);
        Serial.print("; ");
        Serial.print("Abtastrate  = ");
        Serial.print(sampleRate1);
        //Serial.print(sampleRate1);
        Serial.print("; ");
        Serial.print("Pulsweite  = ");
        Serial.print(pulseWidth1);
        //Serial.print(pulseWidth1);
        Serial.print("; ");
        Serial.print("ADC Range  = ");
        Serial.print(adcRange1);
 
      }
 
 
      std::string received_message = "Werte empfangen!";
      pCharacteristic->setValue(received_message);
      pCharacteristic->notify();
      updateSensor = true;
    }
 
};

 
void updateSensorConfig() {
  particleSensor.sensorConfiguration(ledBrightness1, sampleAverage1, MODE_MULTILED, sampleRate1, pulseWidth1, adcRange1);
  Serial.println("Sensor configuration updated");
 }
 
void setup() {
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);
 
  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }
 
  particleSensor.sensorConfiguration(50, SAMPLEAVG_4, MODE_MULTILED, SAMPLERATE_1000, PULSEWIDTH_411, ADCRANGE_16384);
 
  BLEDevice::init("ESP_SPO2");
 
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
 
  BLEService *pService = pServer->createService(SERVICE_UUID);
 
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
 
  pCharacteristic3 = pService->createCharacteristic(
                       CHARACTERISTIC_UUID3,
                       BLECharacteristic::PROPERTY_READ   |
                       BLECharacteristic::PROPERTY_WRITE  |
                       BLECharacteristic::PROPERTY_NOTIFY |
                       BLECharacteristic::PROPERTY_INDICATE
                     );
 
  pCharacteristic3->setCallbacks(new MyCallbacks());
 
  pCharacteristic->addDescriptor(new BLE2902());
  pCharacteristic2->addDescriptor(new BLE2902());
  pCharacteristic3->addDescriptor(new BLE2902());
 
  pService->start();
 
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);
  BLEDevice::startAdvertising();
  Serial.println("Waiting for a client connection to notify...");
}
 
void loop() {
  if (Wert <= 99) {
    //Serial.println(Wert);
    data[Wert] = particleSensor.getRed();
    dataIR[Wert] = particleSensor.getIR();
    Wert = Wert + 1;
  } else {
    Wert = 0;
    //Serial.println("100 Werte im Array gesammelt");
    //Serial.println("Bin in vor Schleife Gerät Verbunden");
    //Serial.println();
    pCharacteristic->setValue((uint8_t*)data, sizeof(data));
    pCharacteristic2->setValue((uint8_t*)dataIR, sizeof(dataIR));
    pCharacteristic->notify();
    pCharacteristic2->notify();
    //Serial.println("Sende Daten:");
 
    if (!deviceConnected) {
      Serial.println("ESP nicht verbunden. Daten: ");
 
      for (int i = 0; i < 100; i++) {
        Serial.print(data[i]);
        Serial.print(" ");
        Serial.println();
      }
    }
  }
 
  if (!deviceConnected) {
    delay(500);
    pServer->startAdvertising();
    Serial.println("start advertising");

    if (LED_off_on == 1)

    { digitalWrite(LED_BUILTIN, HIGH); LED_off_on = 0;}

    else
    
    {digitalWrite(LED_BUILTIN, LOW); LED_off_on = 1;}
    
  }
 
  if (updateSensor) {
    updateSensorConfig();
    updateSensor = false;
  }
}
