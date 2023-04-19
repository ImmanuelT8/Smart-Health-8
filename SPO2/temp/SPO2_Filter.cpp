
#include <Arduino.h>
#include "SPO2_Filter.h"



// DC removal //


float MAX30100::meanDiff()



{
  float avg = 0;

  float M; meanDiffFilter_t* filterValues;

  filterValues->sum -= filterValues->values[filterValues->index];
  filterValues->values[filterValues->index] = M;
  filterValues->sum += filterValues->values[filterValues->index];

  filterValues->index++;
  filterValues->index = filterValues->index % MEAN_FILTER_SIZE;

  if(filterValues->count < MEAN_FILTER_SIZE)
    filterValues->count++;

  avg = filterValues->sum / filterValues->count;
  return avg - M;
}



float values;

void MAX30100::setvalues(uint16_t sw)

{

 values = sw; 

}

