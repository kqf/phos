#!/bin/bash

function examine_versions() {
	echo $1
	echo "HERE"
	comm -2 -3 <(sort $1-muon-calo-pass1.txt) <(sort <(sed s/,// < $1-pass1.txt)) > diff-$1.txt

}

function main() {

	for period in {g..p}; do
		echo LHC16$period-pass1.txt
		examine_versions LHC16$period
	done
}


main