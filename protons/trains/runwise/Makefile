OUTFILE := LHC16g.root
DATASET := LHC16g
OUTDIR = results/data/trigger_qa4

upload:
	$(call upload_result,$(OUTFILE),$(DATASET))

all:
	./download.sh

clean:
	rm -rf *.root LHC*/

define upload_result
	mv $(1).root $(2).root
	-alien_mkdir -p $(ALIEN_HOME)/$(OUTDIR)/
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)/$(OUTDIR)/@ALICE::GSI::SE2
endef
