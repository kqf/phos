# TODO: Estimate the statistics, is DPART parameter is redundant here?
PRODUCTION = 1
DPART = first


grid: | %.cxx
	root -l -b -q 'run.C("$(PRODUCTION)", "grid", "full", "$(DPART)", kTRUE)' || $(call unlink) 
	@echo $(PRODUCTIONs) $(DPART) >> started_jobs.log
	@$(call unlink) && echo "Directory is clean"
	@echo "Started grid analysis" >> .runhistory
	@echo -e "\a"


%.cxx:
	@$(call unlink)	
	@$(call link_sources,../analysis-task-pp,AddAnalysisTaskPP.C "*.h" "*.cxx")


terminate: | %.cxx
	root -l -q 'run.C("$(PRODUCTIONs)", "grid", "terminate", "$(DPART)", kTRUE)' || $(call unlink) 
	@$(call unlink) && echo "Directory is clean"
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"


download: | %.cxx
	root -l -q 'run.C("$(PRODUCTIONs)", "grid", "terminate", "$(DPART)", kTRUE, kFALSE)' || $(call unlink) 
	make upload
	@$(call unlink) && echo "Directory is clean"
	@echo "Terminated grid analysis" >> .runhistory
	@echo -e "\a"


test: | %.cxx
	root -l -q 'run.C("$(PRODUCTIONs)", "local", "test", "$(DPART)", kTRUE)' || $(call unlink) 
	@echo "Local analysis" >> .runhistory
	@$(call upload_result,AnalysisResults,test-analysis-pp)
	@ln -s ../../misc-tools/drawtools/compare.py .
	@# There are problems with python under alienv environment
	@# Therefore it's necessary to use all these tweaks
	./compare.py reference.root test-analysis-pp.root $(TEST_SELECTION) 2> /dev/null | grep -v Aborted  || echo 'Finished!' 
	@$(call unlink) && echo "Directory is clean"
	@echo -e "\a"

upload:
	$(call upload_result,AnalysisResults,$(PRODUCTIONs))

clean:
	rm *.so *.d *~ Task*


define unlink
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
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)@ALICE::GSI::SE2
endef


