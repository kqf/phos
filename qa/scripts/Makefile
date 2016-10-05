# Order-only prerequisite is marked by "|" character

PERIOD=LHC16k
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-2gev-good
# NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-triggerQA
# FILE_NAME=TriggerQA.root
FILE_NAME=CaloCellsQA2.root
DIRECTORY=../results/$(PERIOD)/$(NAME)
IM = $(DIRECTORY)/images

allplots: | $(DIRECTORY)/CaloCellsQA.root 
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	mv *.move.* $(IM)
	@echo -e "\x07"

$(DIRECTORY)/CaloCellsQA.root: | $(DIRECTORY)
	# Merge all outputs
	root -l -b -q 'merge.C("$(DIRECTORY)")'

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download.sh phosqa-$(NAME) $(FILE_NAME) $(DIRECTORY)
	@echo -e "\x07"

trigger: | $(DIRECTORY)
	root -l -b -q  merge.C'("$(DIRECTORY)", "TriggerQA" , "L0")'


badmap: | ../qa-task/getRunsBadCells.C
	root -l -b -q  'getBadMap.C("$(PERIOD)")'
	mv BadMap_$(PERIOD).root ../results/$(PERIOD)

initmap: ../results/$(PERIOD)/REFERENCE_BadMap_$(PERIOD).root
	root -l -b -q  'getBadMap.C("$(PERIOD)", "$<")'

compare: | ../results/$(PERIOD)/goodruns.csv
	./explore-treding-plots.py ../results/$(PERIOD) $(IM)


clean:
	rm -f *.pdf *.eps *.png 
	rm -rf $(DIRECTORY)/{0..10000}.root
	rm -f $(IM)/Makefile

reset:
	rm -rf $(DIRECTORY)/Trigger*
	rm -rf $(DIRECTORY)/Calo*
	rm -rf $(IM)/*

reset-hard: 
	rm -rf $(DIRECTORY)

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
	@convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.png
	@montage -tile 4x1 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass.png
	@montage -tile 2x2 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass4.png
	@convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.png
	@convert -resize 999x333 $(IM)/totmass4.png $(IM)/totmass4.pdf
	@convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.pdf
	@convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.pdf
	@convert $(IM)/hNEventsPerRunIndex.png $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(IM)/hPi0NumRuns.png $(IM)/hPi0MassSigmaRuns.png $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/$(NAME).png
	@echo -e "$(PERIOD).pdf:\n\tpdfunite hNEventsPerRunIndex.pdf ClusterAveragesRuns_NC1_Emin=*_corr4accept.pdf hPi0NumRuns.pdf hPi0MassSigmaRuns.pdf pi0fits.pdf totmass.pdf $(PERIOD).pdf" > $(IM)/Makefile
	@echo -e "\x07"
