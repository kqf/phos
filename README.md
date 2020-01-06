# Photon analysis using PHOS dectector [![Build Status](https://travis-ci.com/kqf/phos.svg?token=7bkqqhrPB19pD1YKrAZM&branch=master)](https://travis-ci.com/kqf/phos)

Main repository consists of several scripts, analysis tasks and various utilities. The outputs from some scripts serve as an input (explicitly or not) to other scripts. Therefore all these tasks should be maintained simultaneously.


## Roadmap

- [x] Quality assurance ([QA](qa/)) of the reconstructed PHOS data.
  - [x] Map of bad channels.  
  - [x]  Check stability of the observables in time.
 
- [x] Neutral pion and $\eta$ [meson production](analysis)
  - [x] Grid [analysis task](protons)
  - [x] Timing cut efficiency study
  - [x] Raw uncorrected yield extraction
  - [x] Acceptance and neutral pion reconstruction efficiency evaluation
    - [x] Single particle Monte-Carlo generation
    - [x] Nonliearity correction
    - [x] Efficiency calculation
    - [x] Feed-down correction
    - [x] Corrected yield extraction
  - [x] Systematic uncertainties estimation
    - [x] Corrected yiled extraction
    - [x] Timing cut efficiency
    - [x] Feed-down correction
    - [x] Nonlinearity correction
    - [x] Global energy scale
    - [x] Acceptance
    - [x] Matherial budget

- [x] Analysis
  - [x] Phenomenological description
  - [x] Previous experiments
  - [x] Theory predictions
  - [ ] Scaling laws
