SEED=6543

MHOME=/alice/cern.ch/user/o/okovalen
REPO=FastGen_pp
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)
FILES = readKine.C fastGen_pp.C fastsim_pp.sh gen.jdl 

upload:
	alien_rmdir $(MHOME)/$(REPO)
	alien_mkdir $(MHOME)/$(REPO)/
	$(foreach file, $(FILES), alien_cp -n $(file) alien:$(MHOME)/$(REPO)/;)

generated.root:
	mkdir -p tmp_results/
	./download.sh $(OUTPUT) generated.root
	ls -ltr tmp_results | wc -l
	hadd generated.root tmp_results/*.root 
	echo -e "\x07"

clean:
	rm -rf tmp_results
	rm -f *.root *~ 