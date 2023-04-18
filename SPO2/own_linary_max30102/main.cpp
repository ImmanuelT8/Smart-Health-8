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


bool Zykluspruefer;
float R; 
float Spo2;

void setup()
{
  //Init serial 
  Serial.begin(115200);

  while (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found");
    delay(1000);
  }

 
  particleSensor.sensorConfiguration(/*ledBrightness=*/0x1F, /*sampleAverage=*/SAMPLEAVG_4, \
                                  /*ledMode=*/MODE_MULTILED, /*sampleRate=*/SAMPLERATE_400, \
                                  /*pulseWidth=*/PULSEWIDTH_411, /*adcRange=*/ADCRANGE_4096);

}


void loop()
{
  ersterSensor_rot.setSensorwert (particleSensor.getRed());
  ersterSensor_IR.setSensorwert (particleSensor.getIR());

  
  Zykluspruefer = ersterSensor_rot.getimzyklus();
  ersterSensor_rot.average();  //ruft die Average Funktion auf um im Zyklus zu aktualisieren
  ersterSensor_IR.average();  //ruft die Average Funktion auf um im Zyklus zu aktualisieren



  if (!Zykluspruefer) 

  {


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
    Serial.println(ersterSensor_IR.startecalculationPIndex());


    R = (ersterSensor_rot.startecalculationAC()/ersterSensor_rot.startecalculationDC())/(ersterSensor_IR.startecalculationAC()/ersterSensor_IR.startecalculationDC()); 
    // Berechnung vom R Wert (AC/DC)//(AC_IR/DC_IR)

    Serial.print("R = ");
    Serial.println(R);

    Spo2 = 110-25*R; //Berechnung von SPO2

    Serial.print("Spo2 = ");
    Serial.println(Spo2);

    Serial.print(" ");
   
  } 

  
}
