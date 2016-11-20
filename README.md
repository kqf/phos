# Photon analysis using PHOS dectector

Main repository consists of several scripts, analysis tasks and various utilities. The outputs from some scripts serve as an input (explicitly or not) to other scripts. Therefore all these tasks should be maintained simultaneously.


[QA tasks of PHOS DATA](qa/)
----------------------------

This repo depends on official `PHOS_TriggerQA`  and `CaloCellQA` in  `$ALICE_PHYSICS/PWGGA/PHOSTasks/`.
It contains all scripts necessary to obtain map of dead/noisy channels of PHOS.
It also includes QA of PHOS trigger.


[Analysis of pp data](protons)
----------------------------------------------

Analysis of the `AOD`/`ESD` data. 
It requires map of bad channels.
The analysis tasks produce histograms and distributions that should be processed further.


[Neutral meson spectra at 13 TeV](pi0-spectrum)
--------------------------------

This subfolder contains all the macros needed to calculate and plot physical results.
It contains some scripts that extract $\pi^{0}$ raw $p_T$ spectrum.


[Direct photons](direct-photons)
--------------------------------

This is a set of scripts that are needed to extract direct photons spectrum.

