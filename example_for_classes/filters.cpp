/*
  Libary um verschiedene Filter für den MAX 30102 einzubinden und 
bestimmte Werte zu berechnen. (zB Durchschnittlichen Wert pro Zeitinterwall). 
Erstellt am 16.04.23 by I.T. 
*/


#include "Arduino.h"
#include "filters.h"
#include <DFRobot_MAX30102.h>

DFRobot_MAX30102 particleSensor;


float ZyklusSPO2::average() {
   unsigned long currentMillis = millis();
   
   if (currentMillis - previousMillis <= interval)  {
        total_per_cycle = total_per_cycle + particleSensor.getRed();
        cycle = cycle + 1; 
   } else if (cycle > 0) {
        average_per_cycle = total_per_cycle/cycle;
        cycle = 0;
        total_per_cycle = 0;
        previousMillis = currentMillis; 
    }
   return average_per_cycle; // liefert den letzten errechneten Wert zurück
}
