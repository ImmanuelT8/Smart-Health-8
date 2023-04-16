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
    const long interval = 10000; 

    float total_per_cycle = 0; 
   
    unsigned long  previousMillis  = 0; 
    unsigned int cycle = 0; 
    float average() ;
    float average_per_cycle  = 0; 
}; 


#endif
