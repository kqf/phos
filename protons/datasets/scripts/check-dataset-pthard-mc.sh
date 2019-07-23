#!/bin/bash

INFILE=$1
YEAR=2017
PERIOD=${INFILE%%.*}
DATATYPE=sim
PREFIX=''
PASS=''

# For merged Aod
FILEPATH="AOD/*"

# For non-merged Aod
# FILEPATH="*.*"


function dump_run()
{
    lines=$(alien_find /alice/$DATATYPE/$YEAR/$PERIOD/$2/$PREFIX$1/$PASS/$FILEPATH/ -z  -name AliAOD.root | wc -l)
    echo $lines
}

# Here is how we find band and/or good runs
function check_pthard_bins()
{
	for pthard in $(seq 1 1 20); do
		echo -n $pthard " "
	    if (($(dump_run $name $pthard) == 1)); then
	    	echo $1 $pthard >> bad-runs-$PERIOD.log
	    	echo "[Fail] "
	    	return 1
		fi
	done
	echo "[OK] "
	return 0
}


function main()
{
	while read name
	do
		echo -n $name " "
		if check_pthard_bins $name; then
			echo $name >> good-runs-$PERIOD.log
		fi
	done < $INFILE
	echo "Done" $INFILE
}

main
echo -e "\x07"