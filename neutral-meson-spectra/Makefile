.PHONY: integrity-test graphs clean

integrity-test:
	pytest analysis/yield/test_observables.py \
		analysis/tof/efficiency_tag.py \
		analysis/efficiency/spmc_efficiency.py

graphs:
	python -m unittest test.analysis.test_quantities


clean:
	rm -f results/*.pdf signals.root *.pdf *.png input-data/efficiency-*.root *.root input-data/nonlinearity-*.root input-data/tof-cut*.root
	rm -rf results/*
