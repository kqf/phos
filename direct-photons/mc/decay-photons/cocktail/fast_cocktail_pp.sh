#!/bin/bash
if [ $# -gt 0 ]
then
    export CONFIG_SEED=$1
    echo CONFIG_SEED is set to $1
fi

aliroot -b -l -q fastGenEMCocktail_pp.C
aliroot -b -l -q readKine.C
