.PHONY: integrity-test update-datasets clean

integrity-test:
	pytest scripts/yield/observables.py \
		scripts/data/tof.py \
		scripts/efficiency/spmc_efficiency.py

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
	pytest -s scripts/systematics/yields.py
	pytest -s scripts/systematics/nonlinearity.py
	pytest -s scripts/systematics/gscale.py
	pytest -s scripts/systematics/tof.py
	pytest -s scripts/systematics/acceptance.py
	pytest -s scripts/systematics/feeddown.py
	pytest -s scripts/systematics/material.py
	pytest -s scripts/systematics/systematics.py


data:
	pytest -s scripts/data/doublegamma.py
	pytest -s scripts/data/cb_parameters.py
	pytest -s scripts/data/mass_width.py
	pytest -s scripts/data/yields.py
	pytest -s scripts/data/tof.py

clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*
