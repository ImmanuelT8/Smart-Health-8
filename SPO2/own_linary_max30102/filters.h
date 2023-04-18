/*
Libary um verschiedene
/*
  Libary um verschiedene Filter für den MAX 30102 einzubinden und 
bestimmte Werte zu berechnen. (zB Durchschnittlichen Wert pro Zeitinterwall). 
Erstellt am 16.04.23 by I.T. 
*/


#include "Arduino.h"

#ifndef filters_h
#define filters_h



 class ZyklusSPO2 { // Definition der Klasse ZyklusSPO2
  public: 
    const long interval = 7000; 
    float total_per_cycle = 0; 
    float AC = 0; 
    float DC = 0; 
    float PIndex = 0; 
    
    void setSensorwert(uint16_t Sensorwert);
    bool getimzyklus();

    int Sensorwertmaxtemp; 
    int Sensorwertpeakpercylce; 

    float startecalculationAC();
    float startecalculationDC();
    float startecalculationPIndex();


    unsigned long  previousMillis  = 0; 
    unsigned int cycle = 0; 
    float average() ;
    float average_per_cycle; 

    private:

    float Sensorwert;
    bool imzyklus = true;

}; 



#endif
