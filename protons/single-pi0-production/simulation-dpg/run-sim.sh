#!/bin/bash

cp ../*.root .
./dpgsim.sh --run 257893 --mode full --uid 1 --nevents 1 --generator PHOSPi0 --detector PHOS --simulation PHOS --reconstruction PHOS