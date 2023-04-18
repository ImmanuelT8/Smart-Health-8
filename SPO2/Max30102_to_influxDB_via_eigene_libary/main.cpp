/*
Aeternum H. Beispielsketch für MAX30102 SPO2 Kalulation per Zeitinterwall
/*
  Das Programm arbeitet mit dem MAX30102 Sensor un der DF Robot Libary. Es wird über 10 Sekunden ein 
  Zeitinterwall geöffnet und in diesem die Sensordaten der roten LED gesammelt. Daraus wird der 
  Durchschnittswert, der AC und DC Wert und PI und SPO2 errechnet. 
Erstellt am 18.04.23 by I.T. 
*/


#include "DFRobot_MAX30102.h"
#include "filters.h"


DFRobot_MAX30102 particleSensor;

ZyklusSPO2 ersterSensor_rot; //Erzeugt ein erstes Objekt der Klasse ZyklusSPO2 der roten LED
ZyklusSPO2 ersterSensor_IR; //Erzeugt ein erstes Objekt der Klasse ZyklusSPO2 der IR LED

#if defined(ESP32)
  #include <WiFiMulti.h>
  WiFiMulti wifiMulti;
  #define DEVICE "ESP32"
#elif defined(ESP8266)
  #include <ESP8266WiFiMulti.h>
  ESP8266WiFiMulti wifiMulti;
  #define DEVICE "ESP8266"
  #define WIFI_AUTH_OPEN ENC_TYPE_NONE
#endif

#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>



// WiFi AP SSID
#define WIFI_SSID "WLAN1-000727"
// WiFi password
#define WIFI_PASSWORD "swint145!"
// InfluxDB v2 server url, e.g. https://eu-central-1-1.aws.cloud2.influxdata.com (Use: InfluxDB UI -> Load Data -> Client Libraries)
#define INFLUXDB_URL "https://eu-central-1-1.aws.cloud2.influxdata.com"
// InfluxDB v2 server or cloud API authentication token (Use: InfluxDB UI -> Load Data -> Tokens -> <select token>)
#define INFLUXDB_TOKEN "WaewtVI-F6C5vSqGnfoohVujayv_I7Pvu8fFMS9yNRFJtImKz-4DUk8dmQjDS3Izww-eJaxdU4f9WxFiJmpoGw=="
// InfluxDB v2 organization id (Use: InfluxDB UI -> Settings -> Profile -> <name under tile> )
#define INFLUXDB_ORG "1624facbb0d16ca2"
// InfluxDB v2 bucket name (Use: InfluxDB UI -> Load Data -> Buckets)
#define INFLUXDB_BUCKET "ESP32"
// Set timezone string according to https://www.gnu.org/software/libc/manual/html_node/TZ-Variable.html
// Examples:
//  Pacific Time:   "PST8PDT"
//  Eastern:        "EST5EDT"
//  Japanesse:      "JST-9"
//  Central Europe: "CET-1CEST,M3.5.0,M10.5.0/3"
#define TZ_INFO "CET-1CEST,M3.5.0,M10.5.0/3"


// InfluxDB client instance with preconfigured InfluxCloud certificate
InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);
// InfluxDB client instance without preconfigured InfluxCloud certificate for insecure connection 
//InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN);

// Data point
Point sensorReadings("measurements");

float O2;
float Puls;
float O2valid;

bool Zykluspruefer;
float R; 
float Spo2;

float red_max_cyclus;
float IR_max_cyclus;
float red_AC_cyclus;
float red_DC_cyclus;
float IR_AC_cyclus;
float IR_DC_cyclus;

float PI_IR_Cyclus;
float PI_red_Cyclus;

float red_durchschnitt;  
float IR_durchschnitt;  
float TempMAX30102; 



int32_t SPO2; //SPO2
int8_t SPO2Valid; //Flag to display if SPO2 calculation is valid
int32_t heartRate; //Heart-rate
int8_t heartRateValid; //Flag to display if heart-rate calculation is valid 



void setup()
{
Serial.begin(115200);




  // Setup wifi
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to wifi");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();

  

  // Setup wifi
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to wifi");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }

 
  particleSensor.sensorConfiguration(/*ledBrightness=*/0x1F, /*sampleAverage=*/SAMPLEAVG_4, \
                                  /*ledMode=*/MODE_MULTILED, /*sampleRate=*/SAMPLERATE_400, \
                                  /*pulseWidth=*/PULSEWIDTH_411, /*adcRange=*/ADCRANGE_4096);


                                  // Add tags
  sensorReadings.addTag("device", DEVICE);
  sensorReadings.addTag("location", "body");
  sensorReadings.addTag("sensor", "MAXIM30102");

  // Accurate time is necessary for certificate validation and writing in batches
  // For the fastest time sync find NTP servers in your area: https://www.pool.ntp.org/zone/
  // Syncing progress and the time will be printed to Serial.
  timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");

  // Check server connection
  if (client.validateConnection()) {
    Serial.print("Connected to InfluxDB: ");
    Serial.println(client.getServerUrl());
  } else {
    Serial.print("InfluxDB connection failed: ");
    Serial.println(client.getLastErrorMessage());
  }

}


void loop()
{
  ersterSensor_rot.setSensorwert (particleSensor.getRed());
  ersterSensor_IR.setSensorwert (particleSensor.getIR());

  
  ersterSensor_rot.average();  //ruft die Average Funktion auf um im Zyklus zu aktualisieren
  ersterSensor_IR.average();  //ruft die Average Funktion auf um im Zyklus zu aktualisieren



   ersterSensor_rot.cyclustime(); 
   ersterSensor_IR.cyclustime(); 


  Zykluspruefer = ersterSensor_rot.getimzyklus();
  
  Serial.print("im Zyklus = ");
  Serial.print(ersterSensor_rot.getimzyklus());
  Serial.print(ersterSensor_IR.getimzyklus());



  if (!Zykluspruefer) 

  {
/*
    Serial.print("Peakwert red =");
    Serial.println(ersterSensor_rot.Sensorwertpeakpercylce);
    Serial.print("Peakwert IR =");
    Serial.println(ersterSensor_IR.Sensorwertpeakpercylce);
    Serial.print("Durchschnitt pro 10 Sekunden red =");
    Serial.println(ersterSensor_rot.average());  
    Serial.print("Durchschnitt pro 10 Sekunden IR =");
    Serial.println(ersterSensor_IR.average());  
    Serial.print("AC red = ");
    Serial.println(ersterSensor_rot.startecalculationAC());
    Serial.print("AC IR = ");
    Serial.println(ersterSensor_IR.startecalculationAC());
    Serial.print("DC red = ");
    Serial.println(ersterSensor_rot.startecalculationDC());
    Serial.println("DC IR = ");
    Serial.println(ersterSensor_IR.startecalculationDC());
    Serial.print("PI red = ");
    Serial.println(ersterSensor_rot.startecalculationPIndex());
    Serial.print("PI IR = ");
    Serial.println(<ersterSensor_IR.startecalculationPIndex>());
*/

    R = (ersterSensor_rot.startecalculationAC()/ersterSensor_rot.startecalculationDC())/(ersterSensor_IR.startecalculationAC()/ersterSensor_IR.startecalculationDC()); 
    // Berechnung vom R Wert (AC/DC)//(AC_IR/DC_IR)

  //  Serial.print("R = ");
  //  Serial.println(R);

    Spo2 = 110-25*R; //Berechnung von SPO2
    
    /*
    Serial.print("Spo2 = ");
    Serial.println(Spo2);
    Serial.print(" ");
    */




    particleSensor.heartrateAndOxygenSaturation(/**SPO2=*/&SPO2, /**SPO2Valid=*/&SPO2Valid, /**heartRate=*/&heartRate, /**heartRateValid=*/&heartRateValid);


  // Add readings as fields to point
  sensorReadings.addField("O2", SPO2);
  sensorReadings.addField("Puls", heartRate);
  sensorReadings.addField("O2valid", SPO2Valid);
  sensorReadings.addField("pulsevalid", heartRateValid);

  sensorReadings.addField("red_AC_cyclus", ersterSensor_rot.startecalculationAC());
  sensorReadings.addField("red_DC_cyclus", ersterSensor_rot.startecalculationDC());
  sensorReadings.addField("red_max_cylus", ersterSensor_rot.Sensorwertpeakpercylce);
  sensorReadings.addField("PI_red_cyclus", ersterSensor_rot.startecalculationPIndex());
  sensorReadings.addField("red_durchschnitt", ersterSensor_rot.average());

  sensorReadings.addField("IR_AC_cylus", ersterSensor_IR.startecalculationAC());
  sensorReadings.addField("IR_DC_cyclus", ersterSensor_IR.startecalculationDC());
  sensorReadings.addField("IR_max_cylus", ersterSensor_IR.Sensorwertpeakpercylce);
  sensorReadings.addField("PI_IR_cyclus", ersterSensor_IR.startecalculationPIndex());
  sensorReadings.addField("IR_durchschnitt", ersterSensor_IR.average());  

  sensorReadings.addField("R", ersterSensor_IR.average());  
  sensorReadings.addField("Max 30102 Temp", particleSensor.readTemperatureC());  
  sensorReadings.addField("SPO2 own", Spo2);  

  // Write point into buffer
  client.writePoint(sensorReadings);
  Serial.print("Schreibe in Datenbank");


  // Clear fields for next usage. Tags remain the same.
  sensorReadings.clearFields();

  // If no Wifi signal, try to reconnect it
  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("Wifi connection lost");
  }

   
  } 

  
}
