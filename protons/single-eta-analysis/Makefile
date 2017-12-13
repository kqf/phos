DATASET = LHC17j3c2
DPART = first
MC = kTRUE
OUTDIR = results/mc/eta/iteration1/

TEST_SELECTION = PhysTender

grid: | %.cxx
	root -l -b -q 'run.C("$(DATASET)", "grid", "full", "$(DPART)", $(MC))' || $(call funlink) 
	@echo $(DATASET) $(DPART) >> started_jobs.log
	@$(call funlink) && echo "Directory is clean"
	@echo "Started grid analysis" >> .runhistory
	@echo -e "\a"


%.cxx:
	@$(call funlink)	
	@# Dirty?!? hack to avoid grid(plugin) limitations.
	@# Add all necessary taks
	@$(call link_sources,../../qa/qa-task,AddTaskCaloCellsQAPt.C "*.h")
	@$(call link_sources,../analysis-task-pp, "*.h" "*.cxx")
	@$(call link_sources,../../qa/qa-track-averages,AddAnalysisTaskTrackAverages.C "*.h" "*.cxx")


terminate: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC))' || $(call funlink) 
	@$(call funlink) && echo "Directory is clean"
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"


download: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)' || $(call funlink) 
	@# Scale and upload both versions
	-root -l -q 'scaleAnalysisResult.C("AnalysisResults.root", "scaled-")'
	$(call upload_result,AnalysisResults,$(DATASET))
	$(call upload_result,scaled-AnalysisResults,scaled-$(DATASET))

	@$(call funlink) && echo "Directory is clean"
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


clean:
	rm *.so *.d *~ Task* *.xml *.root

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
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)/$(OUTDIR)@ALICE::GSI::SE2
endef


define upload_test
	mv $(1).root $(2).root
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)@ALICE::GSI::SE2
endef

