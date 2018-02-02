#!/bin/bash

INFILE=$1
YEAR=2016
RPERIOD=${INFILE%%.*}
PERIOD=${RPERIOD%%-*}
DATATYPE=data
PREFIX='000'
PASS='pass1'

# For merged Aod
FILEPATH="AOD/*"

# For non-merged Aod
# FILEPATH="*.*"

function show_run()
{
    echo /alice/$DATATYPE/$YEAR/$PERIOD/$PREFIX$1/$PASS/$FILEPATH
}


function dump_run()
{
    lines=$(alien_find /alice/$DATATYPE/$YEAR/$PERIOD/$PREFIX$1/$PASS/$FILEPATH/ -z  -name AliAOD.root | wc -l)

    if [[ $lines -ne 1 ]]; then
    	return 0
    fi

    return 1
}

function main()
{
	while read name
	do
		echo -n $name " "
		if dump_run $name; then
			echo $name"," >> $INFILE.verified.txt
		fi
		show_run $name
	done < $INFILE
	echo "Done" $INFILE
	echo "Size of original dataset" `wc -l $INFILE`
	echo "Size of chiecked dataset" `wc -l $INFILE.verified.txt`
}

main
echo -e "\x07"