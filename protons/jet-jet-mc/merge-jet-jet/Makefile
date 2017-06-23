PERIOD = lhc15g6f
REPO = pp-phos-$(PERIOD)
MHOME=/alice/cern.ch/user/o/okovalen
RESULTS = results-$(PERIOD)

scale: $(RESULTS)
	root -l 'scaleBins.C("$(RESULTS)")'
	hadd $(RESULTS)/$(PERIOD).root $(RESULTS)/$(PERIOD)*.root

clean:
	rm -rf tmp_results
	rm -f *.root *~ 