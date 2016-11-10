DIRECTORY=FastGen_pp
SEED=6543
MPATH=alice/cern.ch/user/o/okovalen/$(DIRECTORY)/output/$(SEED)

generated.root:
	mkdir -p tmp_results/
	./download.sh $(DIRECTORY) $(SEED) generated.root
	ls -ltr | wc -l  tmp_results
	hadd tmp_results/*.root generated.root
	rm -rf tmp_results
	echo -e "\x07"

clean:
	rm -f *.root *~ 