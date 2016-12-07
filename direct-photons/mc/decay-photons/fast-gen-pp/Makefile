SEED=1123444

MHOME=/alice/cern.ch/user/o/okovalen
REPO=FastGen_pp
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)
FILES = readKine.C fastGen_pp.C fastsim_pp.sh gen.jdl 

upload:
	alien_rmdir $(MHOME)/$(REPO)
	alien_mkdir $(MHOME)/$(REPO)/
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
	rm -f *.root *~ 
