DIRECTORY=../results/LHC16/iteration3
BASEPATH = ../../../neutral-meson-spectra/input-data/data
FILEPATH = $(BASEPATH)/LHC16/trigger_qa/iteration3_kphi7/LHC16g-pass1.root



images: | $(DIRECTORY)
	@# Install trigger qa only when it's needed
	@which triggerqa > /dev/null || pip install -e .
	triggerqa --filepath=$(FILEPATH)
	pdfunite fitted-sm1*.pdf fitted-sm1.pdf
	pdfunite fitted-sm2*.pdf fitted-sm2.pdf
	pdfunite fitted-sm3*.pdf fitted-sm3.pdf
	pdfunite fitted-sm4*.pdf fitted-sm4.pdf
	pdfunite turn-on-curve-sm*.pdf turn-on-curve.pdf
	pdfunite trending-tru-sm-*.pdf trending-modules.pdf

	@-rm *-tru*
	@-rm *turn-on-curve-sm*.pdf

	mv *.pdf $(DIRECTORY)
	# mv *.png $(DIRECTORY)
	mv *.root $(DIRECTORY)


$(DIRECTORY):
	mkdir -p $@

clean:
	rm -rf $(DIRECTORY)
