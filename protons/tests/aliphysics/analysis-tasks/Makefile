DATASET = LHC16g-muon-calo-pass1
DPART = first
MC = kTRUE

# DATASET = LHC17d20a1
# DPART = second
# MC = kTRUE

TEST_SELECTION = PhysTender

%.cxx:
	@$(call funlink)	
	@$(call link_sources,../analysis-task-pp, "*.h" "*.cxx")
	ln -s ../analysis-task-pp/macros/AddAnalysisTaskPP.C .

grid: 
	root -l -b -q 'run.C("$(DATASET)", "grid", "full", "$(DPART)", $(MC))' 
	@echo $(DATASET) $(DPART) >> started_jobs.log
	@echo "Started grid analysis" >> .runhistory
	@echo -e "\a"

	
terminate: 
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC))' 
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"


download: 
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)' 
	make upload
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	@mkdir -p tmp 
	@rm -rf LHC16o.root
	@$(call save_runs,$(ALIEN_HOME)/pp-phos-$(DATASET),AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	@rm -rf tmp 
	@echo -e "\x07"


test:
	root -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))' 
	@echo "Local analysis" >> .runhistory
	@$(call upload_result,AnalysisResults,test-analysis-pp)
	@ln -s ../../misc-tools/drawtools/compare.py .
	@# There are problems with python under alienv environment
	@# Therefore it's necessary to use all these tweaks
	./compare.py reference.root test-analysis-pp.root $(TEST_SELECTION) 2> /dev/null | grep -v Aborted  || echo 'Finished!' 
	@echo -e "\a"

upload:
	$(call upload_result,AnalysisResults,$(DATASET))

clean:
	@-rm *.so *.d *~ Task*
	@-$(call funlink)
	@-unlink AddAnalysisTaskPP

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
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)@ALICE::GSI::SE2
endef


define funlink
	find -type l -delete	
endef


