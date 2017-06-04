PRODUCTION = 2
# TODO: Estimate the statistics, is DPART parameter is redundant here?
DPART = second

grid: | %.cxx
	root -l -b -q 'run.C("$(PRODUCTION)", "grid", "full", "$(DPART)", kTRUE)' || make unlink 
	echo $(PRODUCTION) $(DPART) >> started_jobs.log
	@make unlink || echo "Directory is clean"
	echo "Started grid analysis" >> .runhistory
	echo -e "\a"

%.cxx:
	make unlink
	@# Dirty?!? hack to avoid grid(plugin) limitations.
	@# Add all necessary taks
	$(call link_sources,../../qa/qa-task,AddTaskCaloCellsQAPt.C "*.h")
	$(call link_sources,../analysis-task-pp,AddAnalysisTaskPP.C "*.h" "*.cxx")
	$(call link_sources,../../qa/qa-track-averages,AddAnalysisTaskTrackAverages.C "*.h" "*.cxx")

unlink:
	find -type l -delete

terminate: | %.cxx
	root -l -q 'run.C("$(PRODUCTION)", "grid", "terminate", "$(DPART)", kTRUE)' || make unlink
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory
	echo -e "\a"

download: | %.cxx
	root -l -q 'run.C("$(PRODUCTION)", "grid", "terminate", "$(DPART)", kTRUE, kFALSE)' || make unlink
	make upload
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory
	echo -e "\a"

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	mkdir -p tmp 
	rm -rf LHC16o.root
	$(call save_runs,$(ALIEN_HOME)/pp-phos-$(PRODUCTION),AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	rm -rf tmp 
	echo -e "\x07

test: | %.cxx
	root -l -q 'run.C("$(PRODUCTION)", "local", "test", "$(DPART)", kTRUE)'
	echo "Local analysis" >> .runhistory
	$(call upload_result,AnalysisResults,test-analysis-pp)
	$(call upload_result,TrackAverages,test-averages-pp)
	@make unlink || echo "Directory is clean"
	# make compare

upload:
	$(call upload_result,AnalysisResults,$(PRODUCTION))

clean:
	rm *.so *.d *~ Task*

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
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)
endef


