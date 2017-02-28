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

# These are experimental targets. These tests should be used with care.
timecut:
	$(ROOT_PYTHON) -m unittest test.timecut_optimization

check-cut:
	$(ROOT_PYTHON) -m unittest test.timecut_evaluation

selection:
	$(ROOT_PYTHON) -m unittest test.check_physics_selection


clean:
	rm -f results/*.pdf



