#!/bin/bash

YEAR=2017
PERIOD=LHC17c
PASS='pass1'


function find_runs()
{
    alien_find /alice/data/$YEAR/$PERIOD -z -name AliAOD.root | grep -e "/pass1/" | cut -d '/' -f 6 | sort | uniq
}

find_runs
