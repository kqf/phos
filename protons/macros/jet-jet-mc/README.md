Analysis of jet-jet mc-data
==========================

These datasets follow a bit different logic.
It's cruicial to run the code on all the datasets therefore it's better to split steering macros.


## Run

```bash

# On lxplus machine

# Setup the environment
alienv enter VO_ALICE@AliPhysics::<RECENT VERSION OF ALIROOT>


# Obrain token and update the environment
alien-token-init

source /tmp/gclient_env_`id -u $USER`

# Runs full analysis
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
