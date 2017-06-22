PERIOD = lhc15g6f
REPO = pp-phos-$(PERIOD)
MHOME=/alice/cern.ch/user/o/okovalen
RESULTS = results-$(PERIOD)

scale: $(RESULTS)
	root -l 'scaleBins.C("$(RESULTS)")'
	hadd $(RESULTS)/$(PERIOD).root $(RESULTS)/$(PERIOD)*.root

$(RESULTS):
	mkdir -p $(RESULTS)
	for i in $$(alien_ls /$(REPO) | grep $(PERIOD)*.root); do alien_cp alien://$(REPO)/$$i $(RESULTS)/$$i; done	
	echo -e "\x07"

clean:
	rm -rf tmp_results
	rm -f *.root *~ 