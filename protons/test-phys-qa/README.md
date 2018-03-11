Test For QA analysis tasks
=============================

This folder contains macro to run QA + physics analysis on **new** LHC16 data. It differs a bit from the old data.
Therefore it's better to split these macros.


## Run

```bash

# On lxplus machine

# Setup the environment
alienv enter VO_ALICE@AliPhysics::<RECENT VERSION OF ALIROOT>


# Obrain token and update the environment
alien-token-init

source /tmp/gclient_env_`id -u $USER`

# Runs full analysis
# IMPORTANT: Due to grid limitations all datasets are split on two parts
#            Remember that you need to modify DPART variable : put first or second.
make grid
```

## Results
Use the same scripts and code as in the case of new dataset.


```bash
# Ensure that you have proper environment and a valid token
# merge the results 

make terminate 


# Download, merge and upload back the merged result
make download
```


