# Photon analysis using PHOS dectector
Main repository consists of several scripts, analysis tasks and various utilities. The outputs from some scripts serve as an input (explicitly or not) to other scripts. Therefore all these tasks should be maintained simultaneously.


[QA tasks of PHOS DATA](qa/)
----------------------------

This repo depends on official `PHOS_TriggerQA`  and `CaloCellQA` in  `$ALICE_PHYSICS/PWGGA/PHOSTasks/`.  This is the start point of the analysis.
These tasks produce vital data to obtain map of dead/noisy channels of PHOS.



[QA data, map of bad channels, trending/perfomance plots ](qa-results)
------------------------------------------------------------------------

This subdirectory contains a lot of script to retreive information about quality of PHOS data. Also it assembles all the plos/images together into one folder. This step produces map of bad channels and list of runs suitable for real analysis.


[Analysis of pp data](phos-protons)
----------------------------------------------

Analysis of the `AOD` data using map of bad channels extracted by previous analysis. 
Histograms and distributions obtained here should be processed further locally.


[Prompt photons](pi0-spectrum)
--------------------------------

This subfolder contains all the macros to calculate and plot physical results.
Right now it contains some scripts that extract $\pi^{0}$ raw $p_T$ spectrum.