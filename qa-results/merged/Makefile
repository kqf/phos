# Order-only prerequisite is marked by "|" character

PERIOD=LHC16k
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-2gev-good
DIRECTORY=../$(PERIOD)/$(NAME)
IM = $(DIRECTORY)/images

allplots: | $(DIRECTORY)/trending.root $(DIRECTORY)/CaloCellsQA.root
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	# ls -ltr

$(DIRECTORY)/trending.root: | $(DIRECTORY)/CaloCellsQA.root
	mkdir -p $(IM)
	mkdir -p fits
	./form-trending-plots.py $(DIRECTORY)
	rm -fr $(IM)/fits # delete old version
	mv fits $(IM)/

$(DIRECTORY)/CaloCellsQA.root: | $(DIRECTORY)
	# Merge all outputs
	root -l -b -q 'merge.C("$(DIRECTORY)")'

pics:
	./draw-pictures.py
	cd pictures;  pdfunite `ls -tr *.pdf` result.pdf

badmap: | ../../qa/getRunsBadCells.C
	root -l -b -q  'getBadMap.C("$(PERIOD)")'
	mv BadMap_$(PERIOD).root ../$(PERIOD)

initmap: ../$(PERIOD)/REFERENCE_BadMap_$(PERIOD).root
	root -l -b -q  'getBadMap.C("$(PERIOD)", "$<")'

TriggerQASingle.root: 
	root -l -b -q  merge.C'("$(DIRECTORY)", "TriggerQA" , "L0")'

trigger: | TriggerQASingle.root 
	mkdir -p $(IM)
	root -l -b -q  ExtractTriggerQA.C'("$(DIRECTORY)/")'
	./triggers-trending.py $(DIRECTORY)/
	mv *.pdf $(IM)

clean:
	rm *.pdf *.eps *.png

# this one requires alienv
# it's not default tasks as it needs to be run only once
images:  
	# Run Trigger QA
	# make trigger

	# Run QA in full mode
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root", kFALSE)'

	# Extract map of bad channels
	make badmap

	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)

	@  # Hidden operations, don't spoil your output
	@montage -tile 4x1 $(IM)/hPi0Slice*.png  -geometry +0+0 $(IM)/pi0fits.png
	@convert -resize 999x333 $(IM)/pi0fits.png $(IM)/pi0fits.png
	@montage -tile 4x1 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass.png
	@montage -tile 2x2 $(IM)/hMassSM{1..4}.png  -geometry +0+0 $(IM)/totmass4.png
	@convert $(IM)/totmass4.png $(IM)/totmass4.pdf
	@convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.png
	@convert $(IM)/hNEventsPerRunIndex.png $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(IM)/hPi0NumRuns.png $(IM)/hPi0MassSigmaRuns.png $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/$(NAME).png
