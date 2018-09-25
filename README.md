# Photon analysis using PHOS dectector ![status](https://travis-ci.com/kqf/phos.svg?token=7bkqqhrPB19pD1YKrAZM&branch=master)

Main repository consists of several scripts, analysis tasks and various utilities. The outputs from some scripts serve as an input (explicitly or not) to other scripts. Therefore all these tasks should be maintained simultaneously.


## Roadmap

- [x] Quality assurance ([QA](qa/)) of the reconstructed PHOS data.
  1.  Map of bad channels.  
  2.  Check stability of the observables in time.
 
- [x] Neutral pion and $\eta$ [meson production](neutral-meson-spectra)
  - [x] Grid [analysis task](protons)
  - [x] Timing cut efficiency study
  - [x] Raw uncorrected yield extraction
  - [ ] Acceptance and neutral pion reconstruction efficiency evaluation
    - [x] Single particle Monte-Carlo generation
    - [x] Nonliearity correction
    - [ ] Efficiency calculation
    - [ ] Feed-down correction
    - [ ] Corrected yield extraction
  - [ ] Systematic uncertainties estimation
    - [ ] Corrected yiled extraction
    - [ ] Timing cut efficiency
    - [ ] Feed-down correction
    - [ ] Nonlinearity correction
    - [ ] Global energy scale
    - [ ] Acceptance
    - [ ] Matherial budget

- [ ] Measurement of neutral meson production in PHOS trigger events 
  - [ ] Trigger QA
  - [ ] Rejection factor
  - [ ] Trigger efficiency
  - [ ] Systematic uncertanity of the PHOS trigger efficiency estimation
