DIRECTORY=../results/LHC16/iteration2
BASEPATH = ../../../neutral-meson-spectra/input-data/data
FILEPATH = $(BASEPATH)/LHC16/trigger_qa/iteration3_kphi7/LHC16g-pass1.root



images: | $(DIRECTORY)
	@# Install trigger qa only when it's needed
	@which triggerqa > /dev/null || pip install -e .
	triggerqa --filepath=$(FILEPATH)

	mv *.pdf $(DIRECTORY)
	# mv *.png $(DIRECTORY)
	mv *.root $(DIRECTORY)


$(DIRECTORY):
	mkdir -p $@

clean:
	rm -rf $(DIRECTORY)
