#!/bin/bash

set -e

if [ "$#" -lt 4 ]; then
    echo "Error: not enough arguments. Provide:"
    echo "1) path of cmems input file"
    echo "2) path of target horizontal mesh (you can create it with cdo griddes...)"
    echo "3) path of target vertical mesh (text file with list of levels)"
    echo "4) name of outfile"
fi

inputFile=$1

targetHgridPath=$2
    
targetVgridPath=$3 

outFile=$4

# horizontal fill of input file
if [ ! -e hfill_${inputFile} ]; then
    echo "Doing horizontal fill on input file"
    cdo -O setmisstonn ${inputFile} hfill_${inputFile}
else
    echo "hfill file already exists"
fi

# vertical fill of input file
if [ ! -e vfill_${inputFile} ]; then
    echo "Doing vertical fill on input file"
    cdo -O vertfillmiss,method=nearest hfill_${inputFile} vfill_${inputFile}
else
    echo "vfill file already exists"
fi

LEVELS=$(cat ${targetVgridPath})

# horizontal remap
if [ ! -e hremap_vfill_${inputFile} ]; then
    echo "Doing Horizontal remap"
    cdo -O remapbil,${targetHgridPath} vfill_${inputFile} hremap_vfill_${inputFile} 
else
    echo "hremap file elready exists"
fi


if [ ! -e vremap_hremap_vfill_${inputFile} ]; then
    echo "target vertical levels:"
    echo $LEVELS
    echo "Doing Vertical remap"
    cdo intlevelx,level=${LEVELS} hremap_vfill_${inputFile} vremap_hremap_vfill_${inputFile}
else
    echo "vremap file alreay exist"
fi  

echo "Renaming variables"
ncrename -O -v thetao,tn vremap_hremap_vfill_${inputFile}
ncrename -O -v so,sn vremap_hremap_vfill_${inputFile}
ncrename -O -v uo,un vremap_hremap_vfill_${inputFile}
ncrename -O -v vo,vn vremap_hremap_vfill_${inputFile}
ncrename -O -v zos,sshn vremap_hremap_vfill_${inputFile}

# do a further horizontal fill
echo "Another horizontal fill on output file..."
cdo setmisstonn vremap_hremap_vfill_${inputFile} temp_vremap_hremap_vfill_${inputFile}

mv temp_vremap_hremap_vfill_${inputFile} ${outFile}




