#!/bin/bash

if [ $# -gt 0 ]
then
    export CONFIG_SEED=$1
    echo CONFIG_SEED is set to $1
fi



tar -xvf OCDBdrain.tar.gz
echo "Unpacked"

aliroot -b -q sim.C 
aliroot -b -q rec.C 
aliroot -b -q CreateAOD.C 
aliroot -b -q rungrid.C 
