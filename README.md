# Neutral meson measurements with PHOS dectector [![Build Status](https://travis-ci.com/kqf/phos.svg?token=7bkqqhrPB19pD1YKrAZM&branch=master)](https://travis-ci.com/kqf/phos)

This is the main repository that consists of analysis tasks (reduce operations) and scripts responsible for postprocessing.


All analysis scripts are organized in the form of the test functions to solve the problem of automatic discovery.


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
    - [x] Material budget
- [x] Analysis
  - [x] Phenomenological description
  - [x] Previous experiments
  - [x] Theory predictions
  - [x] Scaling laws
