.PHONY: integrity-test update-datasets clean

integrity-test:
	pytest analysis/yield/observables.py \
		analysis/data/tof.py \
		analysis/efficiency/spmc_efficiency.py

update-datasets: phos-download
	phos-download --finput=config/vault/ledger.json --output=.

merge-datasets:
	mkdir input-data/data/merged/$(production)/

	hadd input-data/data/merged/$(production)/LHC16-LHC17-LHC18.root \
		input-data/data/LHC16/$(production)/LHC16.root \
		input-data/data/LHC17/$(production)/LHC17.root \
		input-data/data/LHC18/$(production)/LHC18.root 

	hadd input-data/data/merged/$(production)/LHC16-LHC17.root \
		input-data/data/LHC16/$(production)/LHC16.root \
		input-data/data/LHC17/$(production)/LHC17.root

phos-download:
ifeq (, $(shell which phos-download))
	pip install -r ../misc-tools/io/requirements.txt
	pip install -e ../misc-tools/io
endif

systematics:
	pytest -s analysis/systematics/yields.py
	pytest -s analysis/systematics/nonlinearity.py
	pytest -s analysis/systematics/gscale.py
	pytest -s analysis/systematics/tof.py
	pytest -s analysis/systematics/acceptance.py
	pytest -s analysis/systematics/feeddown.py
	pytest -s analysis/systematics/material.py
	pytest -s analysis/systematics/systematics.py


data:
	pytest -s analysis/data/doublegamma.py
	pytest -s analysis/data/cb_parameters.py
	pytest -s analysis/data/mass_width.py
	pytest -s analysis/data/yields.py
	pytest -s analysis/data/tof.py

clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*
