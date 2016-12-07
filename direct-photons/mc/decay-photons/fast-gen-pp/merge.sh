#!/bin/bash

MYPATH=/alice/cern.ch/user/o/okovalen/FastGen_pp

echo $PWD
echo ls
export PRODUCTION=$1

cd $MYPATH/output
hadd `find output/$PRODUCTION/ generated.root | grep .root` output/$PRODUCTION/generated.root
