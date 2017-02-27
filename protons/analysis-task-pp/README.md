PHOS clusters in proton-proton collisions
========================
Main code for ESD/AOD data analysis.  Includes all necessary scripts to run the task locally, on grid and merger/download the output.

## Environment 
Make sure that you have proper environment. For example:

```bash

# Load alisoft
alienv enter VO_ALICE@AliPhysics::vAN-20170222-1


# Get grid token
alien-token-init; source /tmp/gclient_env_`id -u $USER`
```



## Usage
Look inside `Makefile` for more details.
```bash
# submit your analysis
make grid

# merge output in grid
make terminate


# download the output
make download

# to test on local dataset:
# you should have a valid token to upload your output on grid
make test
```