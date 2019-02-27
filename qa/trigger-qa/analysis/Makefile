DIRECTORY :=../results/LHC16/iteration3
BASEPATH := ../../../neutral-meson-spectra/input-data/data
FILEPATH := $(BASEPATH)/LHC16/trigger_qa/iteration3/

INPUTS := $(wildcard $(FILEPATH)/*.root)
odirs := $(patsubst $(FILEPATH)/%.root,$(DIRECTORY)/%.dir,$(INPUTS))
badmap := $(DIRECTORY)/badmap


all: $(odirs) $(badmap)

$(badmap):
	@which channels > /dev/null || pip install -e .
	channels --filepath=$(FILEPATH)

	pdfunite fitted-sm1-tru*.pdf fitted-sm1.pdf
	pdfunite fitted-sm2-tru*.pdf fitted-sm2.pdf
	pdfunite fitted-sm3-tru*.pdf fitted-sm3.pdf
	pdfunite fitted-sm4-tru*.pdf fitted-sm4.pdf

	mkdir -p $@
	mv *.pdf $@
	mv *.root $@
	

%.dir:
	@# Install trigger qa only when it's needed
	@which triggerqa > /dev/null || pip install -e .
	triggerqa --filepath=$(patsubst $(DIRECTORY)/%.dir,$(FILEPATH)/%.root,$@)

	# Merge badmaps
	pdfunite fitted-sm1-tru*.pdf fitted-sm1.pdf
	pdfunite fitted-sm2-tru*.pdf fitted-sm2.pdf
	pdfunite fitted-sm3-tru*.pdf fitted-sm3.pdf
	pdfunite fitted-sm4-tru*.pdf fitted-sm4.pdf

	pdfunite trending-tru-sm*.pdf trending-modules.pdf
	pdfunite trending-turnon-tru-sm*.pdf trending-turnon.pdf
	@-rm *-tru*.pdf

	mkdir -p $@
	mv *.pdf $@
	mv *.root $@

clean:
	rm -rf $(DIRECTORY)
