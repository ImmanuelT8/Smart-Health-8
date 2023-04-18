/*
  Libary um verschiedene Filter für den MAX 30102 einzubinden und 
bestimmte Werte zu berechnen. (zB Durchschnittlichen Wert pro Zeitinterwall). 
Erstellt am 16.04.23 by I.T. 
*/


#include "Arduino.h"
#include "filters.h"


void ZyklusSPO2::setSensorwert(uint16_t sw){    
    Sensorwert = sw;
 }

bool ZyklusSPO2::getimzyklus()

 {

    return imzyklus; //Liefert den Bool Wert ob das Programm im Zyklus ist oder die Zeit abgelaufen ist 

 }


void ZyklusSPO2::cyclustime() {

      unsigned long currentMillis = millis();

      if (currentMillis - previousMillis <= interval)  {

         imzyklus = true; 
      }

      else

      {
         imzyklus = false; 
         previousMillis = currentMillis;  

         
      }

}


float ZyklusSPO2::average() {
   unsigned long currentMillis = millis();
   
   if (imzyklus)  {
        total_per_cycle = total_per_cycle + Sensorwert;
        cycle = cycle + 1; 
        if (Sensorwert > Sensorwertmaxtemp)

        {
                  Sensorwertmaxtemp = Sensorwert;
        } 


   } else if (cycle > 0) {

        average_per_cycle = total_per_cycle/cycle;
        cycle = 0;
        total_per_cycle = 0; 
        Sensorwertpeakpercylce = Sensorwertmaxtemp;

    }

   return average_per_cycle; // liefert den letzten errechneten Wert zurück
   

}

float ZyklusSPO2::startecalculationAC() {

AC = (Sensorwertpeakpercylce - average_per_cycle)*2;
return AC;

}


float ZyklusSPO2::startecalculationDC() {

DC = (Sensorwertpeakpercylce - AC)*2;
return DC;

}


float ZyklusSPO2::startecalculationPIndex() {

PIndex = (AC/DC)*100;
return PIndex;

}



