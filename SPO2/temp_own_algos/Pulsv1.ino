#include "DFRobot_MAX30102.h"

float w;
float w_old;
float filtered_sensorvalue;

int Sensorwert;
bool positivercyklus;
bool erstekurve;
bool zweitekurve;
bool pulsabgeschlossen;
float AC;
float DC;
float tempPos;
float tempNeg;
float tempMax_ohne_filter;
float peakMax_ohne_filter;

float peakMax;
float peakMin;

float Pulszeit;
float Puls;

unsigned long  previousMillis = 0;
const long interval = 10000; 


DFRobot_MAX30102 particleSensor;

void setup()
{
  //Init serial
  Serial.begin(115200);


  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }

  particleSensor.sensorConfiguration(/*ledBrightness=*/0x1F,
/*sampleAverage=*/SAMPLEAVG_4, \
                                  /*ledMode=*/MODE_MULTILED,
/*sampleRate=*/SAMPLERATE_400, \
                                  /*pulseWidth=*/PULSEWIDTH_411,
/*adcRange=*/ADCRANGE_4096);
}

void loop()
{

unsigned long currentMillis = millis(); 


w = particleSensor.getRed() + 0.99 * w_old;
filtered_sensorvalue = w - w_old;
w_old = w;

  //Serial.print("Variable_1:");
  //Serial.println(filtered_sensorvalue);
 //  Serial.println(particleSensor.getRed());

Sensorwert = filtered_sensorvalue;




if (erstekurve & zweitekurve & Sensorwert > 0) // Puls abgeschlossen

{



peakMax_ohne_filter = tempMax_ohne_filter;

peakMax = tempPos;
peakMin = tempNeg;
tempPos = 0;
tempNeg = 0;

zweitekurve = false;
AC = peakMax - peakMin;
DC = peakMax_ohne_filter - AC;

Pulszeit = currentMillis - previousMillis;
Puls = 60000/Pulszeit;
previousMillis = currentMillis;

}


 if (Sensorwert > 0)

{

positivercyklus = true;
erstekurve = true;
zweitekurve = false;

if (Sensorwert > tempPos)
{ tempPos = Sensorwert; tempMax_ohne_filter = particleSensor.getRed();}

}

else

{ positivercyklus = false;
if (Sensorwert < tempNeg) { tempNeg = Sensorwert; }

}

if (!positivercyklus & erstekurve)

{zweitekurve = true;}



Serial.println(Puls);

}
