emtpy:
	$(ROOT_PYTHON) -m unittest test.playground.test_check_emptybins

pi0:
	$(ROOT_PYTHON) run-pi0-spectrum.py


tag:
	$(ROOT_PYTHON) -m unittest test.cuts.tag_and_probe_tof_efficiency


eta:
	$(ROOT_PYTHON) run-eta-spectrum.py


imass:
	$(ROOT_PYTHON) -m unittest test.test_invariant_mass


clean:
	rm -f results/*.pdf signals.root *.pdf *.png input-data/*.eff
