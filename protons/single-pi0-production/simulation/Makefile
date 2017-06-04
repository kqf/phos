SEED=1123444

MHOME=/alice/cern.ch/user/o/okovalen
REPO=single-pi0-production
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)
FILES = AliGenPHOSlibPlus.h Config.C CreateAOD.C generate.jdl merge.jdl merge.sh pi0_Param_pp_7TeV.root.inp single-pion.sh rec.C sim.C

test:
	./single-pion.sh

upload:
	# -alien_rmdir $(MHOME)/$(REPO)
	alien_mkdir -p $(MHOME)/$(REPO)/
	$(foreach file, $(FILES), alien_cp -n $(file) alien:$(MHOME)/$(REPO)/;)

download:
	mkdir -p results 
	for run in $$(alien_ls /$(OUTPUT) | grep .[0-9]*); do alien_cp alien://$(OUTPUT)/$$run/generated.root results/$$run.root; done	
	rm -rf generated.root
	hadd generated.root results/*.root
	rm -rf results
	echo -e "\x07



clean:
	rm -rf tmp_results
	rm -rf *.root *~ *.log *.so *.d *.ps GRP *.dat
