#!/bin/bash
if [ $# -gt 0 ]
then
    export CONFIG_SEED=$1
    echo CONFIG_SEED is set to $1
fi



aliroot -b -q -l fastGen_pp.C >& gen.log
aliroot -b -q -l readKine.C   >& read.log
