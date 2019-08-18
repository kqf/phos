.PHONY: integrity-test update-datasets clean

integrity-test:
	pytest analysis/yield/observables.py \
		analysis/tof/efficiency_tag.py \
		analysis/efficiency/spmc_efficiency.py


update-datasets: phos-download
	phos-download --finput=config/vault/ledger.json --output=.


phos-download:
ifeq (, $(shell which phos-download))
	pip install -r ../misc-tools/io/requirements.txt
	pip install -e ../misc-tools/io
endif


clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*
