OUTDIR = results/data/LHC18/cell_qa/iteration1

all:
	./download.sh

clean:
	rm -rf *.root LHC*/

upload:
	$(call upload_result,)

# output direcotry, filename.root, where to save
define upload_result
	for ofile in $$(ls *.root); do \
		alien_mkdir -p $(ALIEN_HOME)/$(OUTDIR)/ && \
		alien_cp -n $$ofile alien:$(ALIEN_HOME)/$(OUTDIR)/@ALICE::GSI::SE2 \
	; done
endef
