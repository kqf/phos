.PHONY: integrity-test update-datasets clean

integrity-test:
	pytest analysis/yield/observables.py \
		analysis/data/tof.py \
		analysis/efficiency/spmc_efficiency.py

simple-test:
	pytest -s analysis/yield/observables.py

update-datasets: phos-download
	phos-download --finput=config/vault/ledger.json --output=.

phos-download:
ifeq (, $(shell which phos-download))
	pip install -r ../misc-tools/io/requirements.txt
	pip install -e ../misc-tools/io
endif

systematics:
	pytest analysis/systematics/yields.py
	pytest analysis/systematics/nonlinearity.py
	pytest analysis/systematics/gscale.py
	pytest analysis/systematics/tof.py
	pytest analysis/systematics/acceptance.py # TODO: Update selection
	pytest analysis/systematics/feeddown.py
	pytest analysis/systematics/material.py
	pytest analysis/systematics/systematics.py

clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*
