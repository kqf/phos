Analysis of MC data
-------------------

## Explanation

- [x] Check if the $Z_{\text{vertex}}$ distribution looks the same in MC and in real Data. 
The `zvertex.py` compares all listed MC productions to the real-data distribution.

- [ ] Spectrum shape. Distributions in real data and in MC differ. Therefore 
      we should correct for it. Check `weight.py`.

- [x] Nonlinearity
	- Extract parameters for nonlinearity function `nonlinearity.py`
	- Compare different versions of mc corrected for nonlinearity/weighed `different_versions.py`
	- Compare different MC productions and data`compare_data_mc.py`

- [x] Efficiency
	- Calculate efficiency for different productions `efficiency.py`

- [ ] Contributions from differet sources
	- Compare rates from different sources `pi0_sources.py`
	- Generated spectra of $\pi^{0}$s `generated.py`
	- Reconstructed spectra of $\pi^{0}$s `reconstructed.py`
	- Feed-down correction `feeddown.py`
