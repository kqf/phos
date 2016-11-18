SEED=6543

MHOME=/alice/cern.ch/user/o/okovalen
REPO = cocktail_pp
OUTPUT=$(MHOME)/$(REPO)/output/$(SEED)
FILES = readKine.C fastGenEMCocktail_pp.C

simulate: $(FILES)
	# aliroot -b -l -q fastGenEMCocktail2.C
	aliroot -b -l -q fastGenEMCocktail_pp.C
	aliroot -b -l -q readKine.C
	
	../../../../misc-tools/diff-results.py generated.root  pi0-old.root 2> /dev/null 
	# ../../../../misc-tools/diff-results.py generated.root  eta-old.root 2> /dev/null 
	# ../../../../misc-tools/diff-results.py generated.root  omega-old.root 2> /dev/null 


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