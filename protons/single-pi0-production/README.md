Steering macro single #pi^0$ analysis
=============================

All codes needed for single pion generation are available in the folder `simulation`. 
Everything else remains the same as usual. 


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


