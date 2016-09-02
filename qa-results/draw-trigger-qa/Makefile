# Order-only prerequisite is marked by "|" character

PERIOD=LHC16k
NAME=$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-triggerQA
DIRECTORY=../$(PERIOD)/$(NAME)
IM = $(DIRECTORY)/images

trigger: | $(DIRECTORY)/ratio.root 
	./triggers-trending.py $(DIRECTORY)/

	pdfunite $(IM)/NumberClu_*.pdf $(IM)/$(PERIOD)_NumberClu.pdf
	rm $(IM)/NumberClu_*.pdf	

	pdfunite $(IM)/Number_*.pdf $(IM)/$(PERIOD)_Number.pdf
	rm $(IM)/Number_*.pdf	

	pdfunite $(IM)/ProbabilityClu_*.pdf $(IM)/$(PERIOD)_ProbabilityClu.pdf
	rm $(IM)/ProbabilityClu_*.pdf	

	pdfunite $(IM)/Probability_*.pdf $(IM)/$(PERIOD)_Probability.pdf
	rm $(IM)/Probability_*.pdf	

	pdfunite $(IM)/Triggered_*.pdf $(IM)/$(PERIOD)_Triggered.pdf
	rm $(IM)/Triggered_*.pdf	
	echo "DONE DONE DONE DONE"



$(DIRECTORY)/ratio.root: | $(DIRECTORY)/TriggerQASingle.root
	mkdir -p $(IM)
	root -l -b -q  ExtractTriggerQA.C'("$(DIRECTORY)/")'
	@mv *.pdf $(IM)

	@pdfunite $(IM)/trigger_occupancy_cluster_*.pdf $(IM)/$(PERIOD)_trigger_occupancy_cluster.pdf
	@rm $(IM)/trigger_occupancy_cluster_*.pdf

	@pdfunite $(IM)/trigger_occupancy_*.pdf $(IM)/$(PERIOD)_trigger_occupancy.pdf
	@rm $(IM)/trigger_occupancy_*.pdf


$(DIRECTORY)/TriggerQASingle.root:
	mkdir -p $(DIRECTORY)
	rsync okovalen@lxplus.cern.ch:~/private/phos/qa-result/$(PERIOD)/$(DIRECTORY)/TriggerQASingle.root $(DIRECTORY)


clean:
	rm *.pdf *.eps *.png 

reset:
	rm -rf $(DIRECTORY)/ratio.root
	rm -rf $(DIRECTORY)/ResultsTriggerQA.root

reset_hard: 
	rm -rf $(DIRECTORY)/Trigger*	