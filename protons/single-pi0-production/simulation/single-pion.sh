#!/bin/bash

if [ $# -gt 0 ]
then
    export CONFIG_SEED=$1
    echo CONFIG_SEED is set to $1
fi

aliroot -b -q sim.C 
echo -e "\a"
# aliroot -b -q rec.C 
# echo -e "\a"
# aliroot -b -q tag.C 
# echo -e "\a"
# aliroot -b -q CreateAOD.C 
