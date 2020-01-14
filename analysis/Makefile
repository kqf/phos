
sanity-test:
	pytest --no-stop \
		scripts/yield/observables.py \
		scripts/data/tof.py \
		scripts/efficiency/spmc.py \
		scripts/efficiency/feeddown.py \
		scripts/systematics/ep.py \

datasets: phos-download
	phos-download --finput=config/vault/ledger.json --output=.

merge:
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

clean:
	rm -f *.pdf *.png *.root
	rm -rf results/*


.PHONY: sanity-test datasets clean phos-download clean merge
