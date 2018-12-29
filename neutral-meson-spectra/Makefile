.PHONY: integrity-test graphs clean

integrity-test:
	pytest analysis/yield/test_observables.py \
		analysis/tof/efficiency_tag.py \
		analysis/efficiency/spmc_efficiency.py

clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*
