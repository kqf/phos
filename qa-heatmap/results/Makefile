PERIOD=LHC16k
DIRECTORY=phosqa-$(shell echo $(PERIOD) | tr A-Z a-z)-muon-calo-pass1-heatmap
MPATH=alice/cern.ch/user/o/okovalen/$(DIRECTORY)/output


$(PERIOD)-clusters.pdf: | $(PERIOD)
	for run in $$(ls $(PERIOD) | grep root); do root -l -b -q  saveAsImage.C"(\"$(PERIOD)\", \"$$run\")"; done

$(PERIOD):
	mkdir -p $(PERIOD)
	for run in $$(alien_ls /$(MPATH) | grep 000);do alien_cp alien://$(MPATH)/$$run/AnalysisResults.root $(PERIOD)/$$run.root; done
