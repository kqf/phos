SEED=6543

MHOME=/alice/cern.ch/user/o/okovalen
REPO=FastGen_pp
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)


upload:
	alien_rmdir $(MHOME)/$(REPO)
	alien_mkdir $(MHOME)/$(REPO)/
	alien_cp -n * alien:$(MHOME)/$(REPO)/

generated.root:
	mkdir -p tmp_results/
	./download.sh $(OUTPUT) generated.root
	ls -ltr tmp_results | wc -l
	hadd generated.root tmp_results/*.root 
	echo -e "\x07"

clean:
	rm -rf tmp_results
	rm -f *.root *~ 