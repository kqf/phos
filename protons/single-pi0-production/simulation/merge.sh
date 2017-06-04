#!/bin/bash

# NB: Use this script in extreme cases only

MYPATH=/alice/cern.ch/user/o/okovalen/single-pi0-production/

echo $PWD
echo ls
export PRODUCTION=$1

cd $MYPATH/output
hadd `find output/$PRODUCTION/ generated.root | grep .root` output/$PRODUCTION/generated.root
