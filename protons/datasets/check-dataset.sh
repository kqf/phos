#!/bin/bash

INFILE=$1
YEAR=2016
PERIOD=${INFILE%%.*}
DATATYPE=data
PREFIX='000'
PASS='pass1'

# For merged Aod
FILEPATH="AOD/*"

# For non-merged Aod
# FILEPATH="*.*"


function dump_run()
{
    lines=$(alien_find /alice/$DATATYPE/$YEAR/$PERIOD/$2/$PREFIX$1/$PASS/$FILEPATH/ -z  -name AliAOD.root | wc -l)
    echo $lines
}

# Here is how we find bad and/or good runs
function check_pthard_bins()
{
		echo -n $pthard " "
	    if (($(dump_run $name $pthard) == 1)); then
	    	echo $1 $pthard >> bad-runs-$PERIOD.log
	    	echo "[Fail] "
	    	return 1
	    else return
		fi
	echo "[OK] "
	return 0
}


function main()
{
	while read name
	do
		echo -n $name " "
		if dump_run $name; then
			echo $name >> good-runs-$PERIOD.log
		fi
	done < $INFILE
	echo "Done" $INFILE
	echo "Size of original dataset" `wc -l $INFILE`
	echo "Size of chiecked dataset" `wc -l good-runs-$PERIOD.log`
}

main
echo -e "\x07"