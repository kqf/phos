.PHONY: integrity-test graphs clean

integrity-test:
	$(ROOT_PYTHON) -m unittest -q test.software.test_observables

graphs:
	$(ROOT_PYTHON) -m unittest test.analysis.test_quantities


clean:
	rm -f results/*.pdf signals.root *.pdf *.png input-data/efficiency-*.root *.root input-data/nonlinearity-*.root
