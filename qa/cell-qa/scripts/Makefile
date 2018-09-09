# Order-only prerequisite is marked by "|" character


# TRAIN=345_20180305-1550_child
TRAIN=354_20180320-1238_child
# TRAIN_CHILD=1
# PERIOD=LHC17c

# TRAIN_CHILD=2
# PERIOD=LHC17e

# TRAIN_CHILD=3
# PERIOD=LHC17f

# TRAIN_CHILD=4
# PERIOD=LHC17g

# TRAIN_CHILD=5
# PERIOD=LHC17i

# TRAIN_CHILD=6
# PERIOD=LHC17j

# TRAIN_CHILD=7
# PERIOD=LHC17k

# TRAIN_CHILD=8
# PERIOD=LHC17l

# TRAIN_CHILD=9
# PERIOD=LHC17m

# TRAIN_CHILD=10
# PERIOD=LHC17o

TRAIN_CHILD=11
PERIOD=LHC17r


NAME=iteration2
# NAME=$(shell echo $(PERIOD) | tr A-Z a-z)
# NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-triggerQA
# FILE_NAME=TriggerQA.root
FILE_NAME=CaloCellsQA.root
DIRECTORY=../results/$(PERIOD)/$(NAME)
IM = $(DIRECTORY)/images

allplots: | $(DIRECTORY)/CaloCellsQA.root
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	@ mkdir -p $(IM)
	@ mv *.pdf $(IM)
	@ mv *.png $(IM)
	@ mv *.move.* $(IM)
	@ echo -e "\x07"

$(DIRECTORY)/CaloCellsQA.root: | $(DIRECTORY)
	# Merge all outputs
	root -l -b -q 'merge.C("$(DIRECTORY)")'

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download_trains.sh $(PERIOD) $(DIRECTORY) $(TRAIN)_$(TRAIN_CHILD)
	@echo -e "\x07"

trigger: | $(DIRECTORY)
	root -l -b -q  merge.C'("$(DIRECTORY)", "TriggerQA" , "L0")'


badmap:
	root -l -b -q  'saveBadMap.C("$(PERIOD)")'
	@if [ -f BadMap_$(PERIOD).root ]; then mv BadMap_$(PERIOD).root ../results/$(PERIOD); fi
	
initmap: ../results/$(PERIOD)/REFERENCE_BadMap_$(PERIOD).root
	root -l -b -q  'saveBadMap.C("$(PERIOD)", "$<")'

compare: | ../results/$(PERIOD)/goodruns.csv
	$(ROOT_PYTHON) explore-treding-plots.py ../results/$(PERIOD) $(IM)
	
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
	make clean

	# Run QA in full mode
	mkdir -p fits
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root", kFALSE)'

	# Extract map of bad channels
	make badmap

	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	mv *.move.* $(IM)
	rm -rf $(IM)/fits
	mv fits $(IM)

	@  # Hidden operations, don't spoil your output

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

	@convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.png
	@convert $(IM)/pi0fits.pdf $(IM)/pi0fits.pdf

	@convert $(IM)/hNEventsPerRunIndex.png $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(IM)/hPi0NumRuns.png $(IM)/hPi0MassSigmaRuns.png $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/$(NAME).png
	@convert $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/pi0.png

	@if [ -z $$ALICE_ENV ]; then pdfunite $(IM)/hNEventsPerRunIndex.pdf $(IM)/ClusterAveragesRuns_NC1_Emin=*_corr4accept.pdf $(IM)/hPi0NumRuns.pdf $(IM)/hPi0MassSigmaRuns.pdf $(IM)/$(NAME).pdf ;fi	
	@echo -e "\a"