#ifndef SPO2_Filter_H
#define SPO2_Filter_H

#include <Arduino.h>
#include <Wire.h>
#include <math.h>


#define MEAN_FILTER_SIZE        15  


struct meanDiffFilter_t
{
  float values[MEAN_FILTER_SIZE];
  byte index;
  float sum;
  byte count;
};



class MAX30100 
{
  public:
  float meanDiff(float M, meanDiffFilter_t* filterValues);


private:
  meanDiffFilter_t meanDiffIR;


};



#endif
