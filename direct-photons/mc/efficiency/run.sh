#!/bin/bash

if [ $# -gt 0 ]
then
  export CONFIG_SEED=$1
  echo CONFIG_SEED is set to $1
fi


tar -xvf OCDBdrain.tar.gz

aliroot -b -q sim.C >& sim.log
aliroot -b -q rec.C >& rec.log