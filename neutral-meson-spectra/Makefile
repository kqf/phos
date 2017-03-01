pi0:
	$(ROOT_PYTHON) run-pi0-spectrum.py


eta:
	$(ROOT_PYTHON) run-eta-spectrum.py


imass:
	$(ROOT_PYTHON) -m unittest test.test_invariant_mass


algorithm:
	$(ROOT_PYTHON) -m unittest test.test_check_algorithm


per-module:
	$(ROOT_PYTHON) -m unittest test.test_check_different_modules


pileup:
	$(ROOT_PYTHON) -m unittest test.test_check_pileup_contribution

assymetry:
	$(ROOT_PYTHON) -m unittest test.test_check_assymetry


clean:
	rm -f results/*.pdf
