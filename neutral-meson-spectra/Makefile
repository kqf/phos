.PHONY: integrity-test graphs clean

integrity-test:
	python -m unittest -q analysis.yield.test_observables
	python -m unittest analysis.tof.efficiency_tag

graphs:
	python -m unittest test.analysis.test_quantities


clean:
	rm -f results/*.pdf signals.root *.pdf *.png input-data/efficiency-*.root *.root input-data/nonlinearity-*.root input-data/tof-cut*.root
