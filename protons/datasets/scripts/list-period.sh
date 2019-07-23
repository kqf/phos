#!/bin/bash

YEAR=2018
PERIODS="LHC18b LHC18c LHC18d LHC18e LHC18f LHC18g LHC18h LHC18i LHC18j LHC18k LHC18l LHC18m LHC18n LHC18o LHC18p"
PASS="pass1"


function find_runs()
{
    period=$1
    alien_find /alice/data/$YEAR/$period -z -name AliAOD.root | grep -e "/pass1/" | cut -d '/' -f 6 | sort | uniq
}


function main()
{
    for period in $PERIODS
    do
        echo $period
        find_runs $period > ../$period-$PASS.txt
        wc -l ../$period-$PASS.txt
    done
}


main
