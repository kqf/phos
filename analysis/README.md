# Analysis scripts

This folder contains the scripts for the nuetral meson spectra extraction from the histograms created by the grid-selection [tasks](/protons/). The scripts are implemented in the form of unit tests with fixtures (usually data) to solve the problem of the automatic discovery.


## Datasets
These are the steps to download the datasets in use. 
```
# login to the lxplus machine
lxplus

# On lxplus machine: activate the alice-analysis specific environment
alice

# On lxplus machine: download the data to lxplus
alien2datasets
```

Once previous steps are finished, on the local machine, go to the analysis folder

```
# Setup the environment variables that are needed by scripts
export LXPLUS_USER = ...
export LXPLUS_HOME = the "~" folder at lxplus

# Generate a valid ticket for password-less authentification
kinit ${LXPLUS_USER}@CERN.CH

# Download the data from lxplus
make datasets

```
