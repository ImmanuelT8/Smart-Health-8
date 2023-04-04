
#include <Arduino.h>
#include <DFRobot_MAX30102.h>
#include <Wire.h>
#include "Protocentral_MAX30205.h"
MAX30205 tempSensor;

float Signalmax = 1;
float Signalpeak = 1;
float DC;
float AC;
float Summeinterwall = 0;
float Signal; 
float Durchgang;
float Perfusionsindex;
float Signalmin;
float Interwalldurchschnitt;

float Interwalldurchschnitt_IR;
float Summeinterwall_IR = 0;
float DC_IR;
float AC_IR;
float Perfusionsindex_IR;
float Signalpeak_IR = 1;
int Signal_IR;

float Signalmax_IR = 1;
float Signalmin_IR =1;

unsigned long  previousMillis = 0;
float readTemperatureC;
float TempC;

float R;
float Spo2_2;

//#define MAX30205_ADDRESS1        0x49  // 8bit address converted to 7bit
//#define MAX30205_ADDRESS1        0x48  // 8bit address converted to 7bit

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
#define INFLUXDB_TOKEN "JfqFz5i0hYPkSiAkOpEOhWUU2UVX696Jl8bBfAeiDLr38ZxBfc0JDVm2FNS-Paa3E1rDmSuW1eHwxFqufwoV-Q=="
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

//
DFRobot_MAX30102 particleSensor; // I2C

float O2;
float Puls;
float O2valid;
float PerfusI;
float Perfusion;
float temperature;

// Initialize MAX30102 //

void initparticleSensor(){
  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }

   /*!
   *@brief Use macro definition to configure sensor 
   *@param ledBrightness LED brightness, default value: 0x1F（6.4mA), Range: 0~255（0=Off, 255=50mA）
   *@param sampleAverage Average multiple samples then draw once, reduce data throughput, default 4 samples average
   *@param ledMode LED mode, default to use red light and IR at the same time 
   *@param sampleRate Sampling rate, default 400 samples every second 
   *@param pulseWidth Pulse width: the longer the pulse width, the wider the detection range. Default to be Max range
   *@param adcRange ADC Measurement Range, default 4096 (nA), 15.63(pA) per LSB
   */
  particleSensor.sensorConfiguration(/*ledBrightness=*/255, /*sampleAverage=*/SAMPLEAVG_4, \
                        /*ledMode=*/MODE_MULTILED, /*sampleRate=*/SAMPLERATE_100, \
                        /*pulseWidth=*/PULSEWIDTH_411, /*adcRange=*/ADCRANGE_16384);

}


int32_t SPO2; //SPO2
int8_t SPO2Valid; //Flag to display if SPO2 calculation is valid
int32_t heartRate; //Heart-rate
int8_t heartRateValid; //Flag to display if heart-rate calculation is valid 

void loop0() {  }


//Setup for the MAX30102 and InfluxDB

void loop1() {
 // function1

Signal = (particleSensor.getRed());
Signal_IR = (particleSensor.getIR());

 unsigned long currentMillis = millis(); 
 const long interval = 10000; 


  if (currentMillis - previousMillis <= interval) 
  
  {  

//Interwall Signalmax RED gewinnen //

    Serial.print("im Interwall");
    Serial.print("Zeit =");
    Serial.print(currentMillis);
    Serial.print('\n');

    if (Signal > Signalmax) { Signalmax = Signal; }
    if (Signal < Signalmin) { Signalmin = Signal; }

    Summeinterwall = Summeinterwall + Signal;
    Durchgang = Durchgang + 1;

    Serial.print("Summeinterwall = ");
    Serial.print(Summeinterwall);  
    Serial.print("Durchgang = ");
    Serial.print(Durchgang);
    Serial.print('\n');


// Interwall Signalmax IR gewinnen //

if (Signal_IR > Signalmax_IR) { Signalmax_IR = Signal_IR; }
    if (Signal_IR < Signalmin_IR) { Signalmin_IR= Signal_IR; }

    Summeinterwall_IR = Summeinterwall_IR + Signal_IR;
  
    Serial.print("Summeinterwall IR = ");
    Serial.print(Summeinterwall_IR);  
    Serial.print('\n');

    
    
  }

  else

  { 

    Serial.print("Interwall abgelaufen");
    Serial.print('\n');

    Serial.print("Signalmax = ");
    Serial.print(Signalmax);

 
    Interwalldurchschnitt = (Summeinterwall/Durchgang); 
 

    AC = (Signalmax - Interwalldurchschnitt)*2;
    Serial.print("AC = ");
    Serial.print(AC);
    Serial.print('\n');

    DC= Signalmax-AC;
    Serial.print("DC = ");
    Serial.print(DC);
    Serial.print('\n');


    Perfusionsindex = (AC/DC)*100;
    Serial.print("Perfusionsindex");
    Serial.print(Perfusionsindex);
    Serial.print('\n');


    Serial.print("Signalmax IR = ");
    Serial.print(Signalmax_IR);

    Interwalldurchschnitt_IR = (Summeinterwall_IR/Durchgang); 

    AC_IR = (Signalmax_IR - Interwalldurchschnitt_IR)*2;
    Serial.print("AC IR = ");
    Serial.print(AC_IR);
    Serial.print('\n');

    DC_IR= Signalmax_IR-AC_IR;
    Serial.print("DC IR = ");
    Serial.print(DC_IR);
    Serial.print('\n');
    R = (AC/DC)/(AC_IR/DC_IR);

    Spo2_2 = 110-25*R;






  //float temp = tempSensor.getTemperature(); // read temperature for every 100ms
	//Serial.print(temp ,2);
	//Serial.println("'c" );

   // Add readings as fields to point
 // sensorReadings.addField("Temperatur", temp);




 // Write point into buffer
  client.writePoint(sensorReadings);

  // Clear fields for next usage. Tags remain the same.
  sensorReadings.clearFields();

    // If no Wifi signal, try to reconnect it
  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("Wifi connection lost");
  }

      particleSensor.heartrateAndOxygenSaturation(/**SPO2=*/&SPO2, /**SPO2Valid=*/&SPO2Valid, /**heartRate=*/&heartRate, /**heartRateValid=*/&heartRateValid);


if (SPO2Valid > 0)

{

  TempC = particleSensor.readTemperatureC();
  // Add readings as fields to point
  sensorReadings.addField("O2", SPO2);
  sensorReadings.addField("Puls", heartRate);
  sensorReadings.addField("O2valid", SPO2Valid);
  sensorReadings.addField("Perfusion", Perfusionsindex);
  sensorReadings.addField("MaximTempC", TempC);
  sensorReadings.addField("AC red", AC);
  sensorReadings.addField("DC red", DC);
  sensorReadings.addField("AC IR", AC_IR);
  sensorReadings.addField("DC IR", DC_IR);
  sensorReadings.addField("Perfusion IR", Perfusionsindex_IR);
  sensorReadings.addField("Temp Max 30102", TempC);
  sensorReadings.addField("R", R);
  sensorReadings.addField("Spo2 II",  Spo2_2);
  




 // temperature = particleSensor.getTemperature_C();

//   sensorReadings.addField("MAX_Temp", temperature);




}

else { sensorReadings.addField("O2valid", SPO2Valid);  sensorReadings.addField("Perfusion", Perfusionsindex);
}
  

  // Add readings as fields to point
  
  // Print what are we exactly writing
  Serial.print("Writing: ");
  Serial.println(client.pointToLineProtocol(sensorReadings));
  
  
  Serial.print(F("heartRate="));
  Serial.print(heartRate, DEC);
  Serial.print(F(", heartRateValid="));
  Serial.print(heartRateValid, DEC);
  Serial.print(F("; SPO2="));
  Serial.print(SPO2, DEC);
  Serial.print(F(", SPO2Valid="));
  Serial.println(SPO2Valid, DEC);
  Serial.print("TemperatureC=");
  Serial.print(TempC, 4);

  
  // Write point into buffer
  client.writePoint(sensorReadings);

  // Clear fields for next usage. Tags remain the same.
  sensorReadings.clearFields();

  // If no Wifi signal, try to reconnect it
  if (wifiMulti.run() != WL_CONNECTED) {
    Serial.println("Wifi connection lost");
  }

  
    previousMillis = currentMillis; 
    Serial.print("Aktuelle Zeit auf vorherige gesetzt =");
    Serial.print(previousMillis); 
    Serial.print('\n');

    Signalmax = 1; Summeinterwall = 1; Durchgang = 0;


}
 }

void setup1() { 

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
  
  //Init MAXIM sensor
  initparticleSensor();
  
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

 
 //Setup for the MAX30205

//void setup2() {

 //Wire.begin();

  //scan for temperature in every 30 sec untill a sensor is found. Scan for both addresses 0x48 and 0x49
  //while(!tempSensor.scanAvailableSensors()){
  //  Serial.println("Couldn't find the temperature sensor, please connect the sensor." );
   // delay(30000);
 // }//

  //tempSensor.begin();   // set continuos mode, active mode

 //}


void setup() {


 setup1(); 
 //setup2();

}


void loop() {
  loop0();   // for testing only
  loop1();   // for testing only
}
