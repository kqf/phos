# Single Particle MC

For the efficiency/performance reasons single particle MC was generated in two different $p_T$ ranges: low ( $0 < p_T < 8$ GeV/c) and high ($8 < p_T < 100$ GeV/c).
This complicates analysis of the single particle MC.


Here are the steps that are needed to run the code.

- [x] Compare $p_T$ distributions in different ranges and try to choose optimal join point. Dedicated script: `mass_width.py`
- [x] Choose right joining point for efficiency. Use `mc/single/overlap_region.py`
- [x] Nonlinearity study
- [ ] Weights for single particle mc
