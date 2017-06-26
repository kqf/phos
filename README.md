# Photon analysis using PHOS dectector

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
  - [ ] Corrected yield extraction
  - [ ] Systematic uncertainties estimation

- [ ] Measurement of the [direct photon](direct-photons) spectrum 
  - [ ] Photon raw yield extraction
  - [ ] Photon registration efficiency
  - [ ] Decay photon spectrum estimation 
  - [ ] $\gamma/\pi^0$ ratio evaluation
  - [ ] Systematic error estimation 
