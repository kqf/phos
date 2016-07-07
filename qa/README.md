PHOS QA Analysis task
=====================

Modified version of `$ALIPHYSICS/PWGGA/PHOSTasks/CaloCellQA/` code.
This version differs from [original code](http://git.cern.ch/pubweb/AliPhysics.git/tree/HEAD:/PWGGA/PHOSTasks/CaloCellQA):

* It applies additional cuts on PHOS clusters: $P_{T} > 1$ GeV/c and $P_{T} > 2$ GeV/c.
* Both versionas are saved to `CaloCellsQA1.root` and `CaloCellsQA2.root`  files.
* Added some extra lines in macro (physics selection, alien plugin etc.)
* In order to check your data use `check_dataset.sh` simple macro to test your dataset. TODO: Find a standard aliroot tool to do this.