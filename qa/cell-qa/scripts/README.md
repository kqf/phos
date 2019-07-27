QA scripts
----------

This directory contains set of scrits needed to find bad/noisy channels and for final QA outputs. 
All scripts should be invoked through the `Makefile` after updating appropriate varaibles.


## Usecases

```bash


# Download/merge/convert per-run output created by qa-task and extract! noisy cells
make

# Delete per-run *.root files but leave merged results
make clean

# Form final plots 
make images

# If you are only interested in final plots
make; make clean; make images

# Save iteration provided that you have saved previous result in a folder ../results/LHC16x/iteration1
make save-iteration

# If something went wrong and you want to delete your working folder
make reset-hard

# To compare your trend plots with alice logbooc data (saved in .csv file, see Makefile for the details)
make compare

# To get list of absolute id's of bad channels from ROOT file 
make init-map
```

## Run the multiple datasets
```
# Use ROOT6 environment to merge the datasets to avoid io issues
alice
./run-all.sh

# Use ROOT5 environment to make the plots
alice-debug
makeoption=images ./run-all.sh
```
