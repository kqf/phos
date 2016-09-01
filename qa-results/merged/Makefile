# Order-only prerequisite is marked by "|" character

PERIOD=LHC16k
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-trigger
FILE_NAME=TriggerQA.root
# FILE_NAME=CaloCellsQA2.root
DIRECTORY=../$(PERIOD)/$(NAME)
IM = $(DIRECTORY)/images

allplots: | $(DIRECTORY)/CaloCellsQA.root 
	root -l -b -q  getCellsRunsQAPHOS.C'("$(DIRECTORY)/CaloCellsQA.root")'
	mkdir -p $(IM)
	mv *.pdf $(IM)
	mv *.png $(IM)
	mv *.move.* $(IM)
	@echo -e "\x07"

$(DIRECTORY)/CaloCellsQA.root: $(DIRECTORY)
	# Merge all outputs
	root -l -b -q 'merge.C("$(DIRECTORY)")'

$(DIRECTORY):
	mkdir -p $(DIRECTORY)
	./download.sh phosqa-$(NAME) $(FILE_NAME) $(DIRECTORY)
	@echo -e "\x07"

badmap: | ../../qa/getRunsBadCells.C
	root -l -b -q  'getBadMap.C("$(PERIOD)")'
	mv BadMap_$(PERIOD).root ../$(PERIOD)

initmap: ../$(PERIOD)/REFERENCE_BadMap_$(PERIOD).root
	root -l -b -q  'getBadMap.C("$(PERIOD)", "$<")'

$(DIRECTORY)/TriggerQASingle.root: | $(DIRECTORY)
	root -l -b -q  merge.C'("$(DIRECTORY)", "TriggerQA" , "L0")'

$(DIRECTORY)/ratio.root:
	mkdir -p $(IM)
	root -l -b -q  ExtractTriggerQA.C'("$(DIRECTORY)/")'
	@mv *.root $(DIRECTORY)
	@mv *.pdf $(IM)

	@pdfunite $(IM)/trigger_occupancy_cluster_*.pdf $(IM)/$(PERIOD)_trigger_occupancy_cluster.pdf
	@rm $(IM)/trigger_occupancy_cluster_*.pdf

	@pdfunite $(IM)/trigger_occupancy_*.pdf $(IM)/$(PERIOD)_trigger_occupancy.pdf
	@rm $(IM)/trigger_occupancy_*.pdf


trigger: | $(DIRECTORY)/ratio.root 
	./triggers-trending.py $(DIRECTORY)/

	@pdfunite $(IM)/NumberClu_*.pdf $(IM)/$(PERIOD)_NumberClu.pdf
	@rm $(IM)/NumberClu_*.pdf	

	@pdfunite $(IM)/Number_*.pdf $(IM)/$(PERIOD)_Number.pdf
	@rm $(IM)/Number_*.pdf	

	@pdfunite $(IM)/ProbabilityClu_*.pdf $(IM)/$(PERIOD)_ProbabilityClu.pdf
	@rm $(IM)/ProbabilityClu_*.pdf	

	@pdfunite $(IM)/Probability_*.pdf $(IM)/$(PERIOD)_Probability.pdf
	@rm $(IM)/Probability_*.pdf	

	@pdfunite $(IM)/Triggered_*.pdf $(IM)/$(PERIOD)_Triggered.pdf
	@rm $(IM)/Triggered_*.pdf	


clean:
	rm *.pdf *.eps *.png 

reset:
	rm -rf $(DIRECTORY)

# this one requires alienv
# it's not default tasks as it needs to be run only once
images:  
	# Run Trigger QA
	# make trigger

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
	@convert $(IM)/totmass4.png $(IM)/totmass4.pdf
	@convert -resize 999x333 $(IM)/totmass.png $(IM)/totmass.png
	@convert $(IM)/hNEventsPerRunIndex.png $(IM)/'ClusterAveragesRuns_NC1_Emin=*_corr4accept.png' $(IM)/hPi0NumRuns.png $(IM)/hPi0MassSigmaRuns.png $(IM)/pi0fits.png $(IM)/totmass.png -append $(IM)/$(NAME).png
	@echo -e "\x07"
