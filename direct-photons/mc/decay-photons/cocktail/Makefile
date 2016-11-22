SEED=123456
GHOME=/alice/cern.ch/user/o/okovalen
REPO = fast-cocktail
OUTPUT=$(GHOME)/$(REPO)/output/$(SEED)

FILES = readKine.C fastGenEMCocktail_pp.C fast_cocktail_pp.jdl fast_cocktail_pp.sh AliGenPHOSMesons.h ParticleKinematics.h

upload:
	-alien_mkdir $(GHOME)/$(REPO)/
	$(foreach file, $(FILES), alien_cp -n $(file) alien:$(GHOME)/$(REPO)/;)

download:
	mkdir -p results 
	for run in $$(alien_ls /$(OUTPUT) | grep .[0-9]*); do alien_cp alien://$(OUTPUT)/$$run/generated.root results/$$run.root; done	
	rm -rf generated.root
	hadd generated.root results/*.root
	rm -rf results
	echo -e "\x07

test:
	# aliroot -b -l -q fastGenEMCocktail2.C
	aliroot -b -l -q fastGenEMCocktail_pp.C
	aliroot -b -l -q readKine.C
	
	-../../../../misc-tools/diff-results.py generated.root  info/pi0-old.root 2> /dev/null 
	# ../../../../misc-tools/diff-results.py generated.root  eta-old.root 2> /dev/null 
	# ../../../../misc-tools/diff-results.py generated.root  omega-old.root 2> /dev/null 

clean:
	rm -f *.root *~  *.so *.d