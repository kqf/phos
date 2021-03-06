# Uncomment to use makefile for each period separately
# year=2018
# period=LHC18b
# name=iteration1

TARGETDIR=/alice/data/$(year)/$(period)
TRAIN=/pass1/AOD208/PWGGA/GA_pp_AOD/$(train)_child_$(child)
DIRECTORY=../results/$(year)/$(period)/$(name)
IM = $(DIRECTORY)/images

$(DIRECTORY)/$(ofilename): | $(DIRECTORY)
	# Merge all outputs
	root -l -b -q 'merge.C("$(DIRECTORY)")'

allplots: | $(DIRECTORY)/$(ofilename)
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/$(ofilename)")'
	@ mkdir -p $(IM)
	@ mv *.pdf $(IM)
	@ mv *.png $(IM)
	@ mv *.move.* $(IM)
	@ echo -e "\x07"

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download_trains.sh $(TARGETDIR) $(DIRECTORY) $(TRAIN)
	@echo -e "\x07"

trigger: | $(DIRECTORY)
	root -l -b -q  merge.C'("$(DIRECTORY)")'


badmap:
	root -l -b -q  'saveBadMap.C("$(period)")'
	@if [ -f BadMap_$(period).root ]; then mv BadMap_$(period).root ../results/$(year)/$(period).root; fi
	
initmap: ../results/$(period)/REFERENCE_BadMap_$(period).root
	root -l -b -q  'saveBadMap.C("$(period)", "$<")'

compare: | ../results/$(period)/goodruns.csv
	$(ROOT_PYTHON) explore-treding-plots.py ../results/$(period) $(IM)
	
inspect-cells: $(CELLS_TO_INSPECT)
	@# assuming that CELLS_TO_INSPECT is a bash varaible
	@# CELLS_TO_INSPECT=../path/to/cells.json
	./convert-xz-to-abs.py $(CELLS_TO_INSPECT)

clean:
	rm -f *.pdf *.eps *.png 
	rm -rf $(DIRECTORY)/*.*.root
	rm -rf $(IM)/*

reset:
	rm -rf $(DIRECTORY)/Trigger*
	rm -rf $(DIRECTORY)/Calo*

reset-hard: 
	rm -rf $(DIRECTORY)

save-iteration:
	@echo 'Last available folder: ' iteration$(shell cd $(DIRECTORY)/../; ls -d iteration* | grep -o '[0-9]*' | sort -g | tail -1)
	@mv $(DIRECTORY) $(DIRECTORY)/../iteration$(shell cd $(DIRECTORY)/../; ls -d iteration* | grep -o '[0-9]*' | sort -g | tail -1 | xargs echo "1 + " | bc)



# this one requires alienv
# it's not default tasks as it needs to be run only once
images:
	# clean the directory befor starting
	# don't merge multiple times
	# make clean

	# Run QA in full mode
	mkdir -p fits
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root", kFALSE)'

	@# Extract map of bad channels
	@# make badmap

	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	mv *.move.* $(IM)
	rm -rf $(IM)/fits
	mv fits $(IM)

	@# Hidden operations, don't spoil your output

	@montage -tile 4x1 $(IM)/hPi0Slice*.png  -geometry +0+0 $(IM)/pi0fits.png
	@montage -tile 4x1 $(IM)/hPi0Slice*.pdf  -geometry +0+0 $(IM)/pi0fits.pdf

	@montage -tile 4x1 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass.png
	@montage -tile 2x2 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass4.png

	@montage -tile 4x1 $(IM)/hMassSM{1..4}.pdf  -geometry +0+0 $(IM)/totmass.pdf
	@montage -tile 2x2 $(IM)/hMassSM{1..4}.pdf  -geometry +0+0 $(IM)/totmass4.pdf

	@convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.png
	@convert $(IM)/totmass.pdf $(IM)/totmass.pdf

	@convert -resize 999x333 $(IM)/totmass4.png $(IM)/totmass4.png
	@convert $(IM)/totmass4.pdf $(IM)/totmass4.pdf

	# @convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.png
	# @convert $(IM)/pi0fits.pdf $(IM)/pi0fits.pdf

	@convert $(IM)/hNEventsPerRunIndex.png \
			 $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' \
			 $(IM)/hPi0NumRuns.png \
			 $(IM)/hPi0MassSigmaRuns.png \
			 $(IM)/totmass.png \
			 -append $(IM)/$(name).png
	# @convert $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/pi0.png

	@if [ -z $$ALICE_ENV ]; then pdfunite $(IM)/hNEventsPerRunIndex.pdf $(IM)/ClusterAveragesRuns_NC1_Emin=*_corr4accept.pdf $(IM)/hPi0NumRuns.pdf $(IM)/hPi0MassSigmaRuns.pdf $(IM)/$(name).pdf ;fi	
	@echo -e "\a"
