#!/bin/bash

# alien_cp alien:///alice/sim/2016/LHC16j2a1/OCDB/257893/OCDBsim.root . 
# alien_cp alien:///alice/sim/2016/LHC16j2a1/OCDB/257893/OCDBrec.root . 
chmod +x dpgsim.sh
./dpgsim.sh --run 257893 --mode full --uid 1 --nevents 1 --generator PHOSPi0 --detector PHOS --simulation PHOS --reconstruction PHOS