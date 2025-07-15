#!/bin/bash

boundaries="east north south_1 south_2 west"


for mem in $(seq -f "%03g" 0 3); do                     # loop over ensemble members
    echo ${mem}
    mkdir -p M${mem}
    cd M${mem}
    for year in `seq 1993 2019`; do                     # loop over years
        mkdir -p $year;                                 # force creation of folder   
        cd $year    
        for month in $(seq -f "%02g" 1 12); do          # loop over months
            mkdir -p ${month}
        done
        cd ..
    done
    cd ..
done
