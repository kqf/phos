 QA Analysis 
=========

Modified version of `$ALIPHYSICS/PWGGA/PHOSTasks/CaloCellQA/` code.
This version differs from [original code](http://git.cern.ch/pubweb/AliPhysics.git/tree/HEAD:/PWGGA/PHOSTasks/CaloCellQA):

* It cam apply additional cuts on PHOS clusters: $p_{T} > 1$ GeV/c and $p_{T} > 2$ GeV/c.
* Both versionas are saved to `CaloCellsQA1.root` and `CaloCellsQA2.root`  files.
* Added some extra lines in macro (physics selection, alien plugin etc.)
* In order to check your data use `check_dataset.sh` simple macro to test your dataset. TODO: Find a standard aliroot tool to do this.

**Now** it also performs tirgger QA. 
It runs trigger qa for all types of triggers L0, and all L1. Original code is here:
[`$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_TriggerQA`](http://git.cern.ch/pubweb/AliPhysics.git/tree/HEAD:/PWGGA/PHOSTasks/PHOS_TriggerQA)


How to ...
-------

```
#!bash

# modify launching run.C for your needs
make grid


# merge TriggerQA.root
make terminate

# store your file for further processing
mv TriggerQA.root ../qa-results/LHC16h

# Cells QA can't be merged this way 
# as it contains run-by-run histograms
# therefore we should merge it manually

# Let's consider LHC16h QA
cd ../qa-results
mkdir -p LHC16h/lhc16h-initial
cd  LHC16h/lhc16h-initial

# once you are inside the directory
#  and you have a valid token
aliensh
cd your-grid-output-dir
counter=1; for f in $(find . -z -name CaloCellsQA2.root); do cp $f file:$((counter++)).root ; done
```


All subsequent steps are (will be ... in neares future) described [here](../qa-results/).
