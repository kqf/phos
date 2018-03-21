# DATASET = LHC16i-muon-calo-pass1
# DPART = second
# MC = kFALSE
# OUTDIR = results/data/corrected/

# DATASET = LHC17d20a2_extra
# DPART = first
# MC = kTRUE
# OUTDIR = results/mc/pythia

# TEST_SELECTION = PhysTender

grid: | %.cxx
	root -l -b -q 'run.C("$(DATASET)", "grid", "full", "$(DPART)", $(MC))' || $(call funlink)
	@echo $(DATASET) $(DPART) >> started_jobs.log
	@$(call funlink) && echo "Directory is clean"
	@echo "Started grid analysis on $(DPART) part of $(DATASET)" >> .runhistory
	@echo -e "\a"


terminate: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC))' || $(call funlink)
	@$(call funlink) && echo "Directory is clean"
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"


download: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)' || $(call funlink)
	make upload
	@$(call funlink) && echo "Directory is clean"
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"

%.cxx:
	$(error The target "$@" is not implemeted, please implement this on your own)

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	@mkdir -p tmp
	@rm -rf LHC16o.root
	@$(call save_runs,$(ALIEN_HOME)/pp-phos-$(DATASET),AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	@rm -rf tmp
	@echo -e "\x07"


test: | %.cxx
	root -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))' || $(call funlink)
	@echo "Local analysis" >> .runhistory
	@$(call upload_test,AnalysisResults,test-analysis-pp)
	@ln -s ../../misc-tools/drawtools/compare.py .
	@# There are problems with python under alienv environment
	@# Therefore it's necessary to use all these tweaks
	./compare.py reference.root test-analysis-pp.root $(TEST_SELECTION) 2> /dev/null | grep -v Aborted  || echo 'Finished!'
	@$(call funlink) && echo "Directory is clean"
	@echo -e "\a"

upload:
	$(call upload_result,AnalysisResults,$(DATASET))

clean:
	$(call funlink)
	rm -f *.so *.d *~ Task*

unlink:
	$(call funlink)


define funlink
	find -type l -delete
endef

# output direcotry, filename.root, where to save
define save_runs
	for run in $$(alien_ls $(1)/output | grep .[0-9]*); do \
		alien_cp alien://$(1)/output/$$run/$(2) $(3)/$$run.root; \
	done
endef


define link_sources
	for file in $(2); do \
		ln -s $(1)/$$file .; \
	done
endef


define upload_result
	mv $(1).root $(2).root
	-alien_mkdir -p $(ALIEN_HOME)/$(OUTDIR)/
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)/$(OUTDIR)/@ALICE::GSI::SE2
endef

define upload_test
	mv $(1).root $(2).root
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)@ALICE::GSI::SE2
endef

