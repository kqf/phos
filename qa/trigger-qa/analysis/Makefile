DIRECTORY :=../results/LHC16/iteration3
BASEPATH := ../../../neutral-meson-spectra/input-data/data
FILEPATH := $(BASEPATH)/LHC16/trigger_qa/iteration3/

INPUTS := $(wildcard $(FILEPATH)/*.root)
ODIRS := $(patsubst $(FILEPATH)/%.root,$(DIRECTORY)/%.dir,$(INPUTS))


all: $(ODIRS)


%.dir:
	@# Install trigger qa only when it's needed
	@which triggerqa > /dev/null || pip install -e .
	triggerqa --filepath=$(patsubst $(DIRECTORY)/%.dir,$(FILEPATH)/%.root,$@)

	# pdfunite fitted-sm1*.pdf fitted-sm1.pdf
	# pdfunite fitted-sm2*.pdf fitted-sm2.pdf
	# pdfunite fitted-sm3*.pdf fitted-sm3.pdf
	# pdfunite fitted-sm4*.pdf fitted-sm4.pdf

	# pdfunite turn-on-curve-sm*.pdf turn-on-curve.pdf
	# pdfunite trending-tru-sm-*.pdf trending-modules.pdf

	@-rm *-tru*
	@-rm *turn-on-curve-sm*.pdf

	mkdir -p $@
	mv *.pdf $@
	mv *.png $@
	mv *.root $@

clean:
	rm -rf $(DIRECTORY)
