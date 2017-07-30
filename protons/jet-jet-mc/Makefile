DATASET = LHC17f8d
DPART = first
MC = kTRUE
PAUSE = 30m

# PtBins = 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 
PtBins = 1 2 13 14 
# PtBins =  9 8 7 6 5 4 3 2 1 
# PtBins = 20

grid: | %.cxx
	$(call jetjet,gridstart,$(DATASET))
	@make unlink || echo "Directory is clean"
	echo -e "\a"

terminate: | %.cxx
	$(call jetjet,terminatestart,$(DATASET))
	@make unlink || echo "Directory is clean"
	echo -e "\a"

download: | %.cxx
	$(call jetjet,downloadstart,$(DATASET))
	make unlink
	hadd scaled-$(DATASET).root scaled-$(DATASET)*.root
	$(call upload_result, scaled-$(DATASET).root)

	hadd $(DATASET).root $(DATASET)*.root
	$(call upload_result, $(DATASET).root)

	echo "Terminated grid analysis" >> .runhistory
	@make unlink || echo "Directory is clean"
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

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	mkdir -p tmp 
	rm -rf LHC16o.root
	$(call save_runs,$(ALIEN_HOME)/pp-phos-$(DATASET),AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	rm -rf tmp 
	echo -e "\x07

test: | %.cxx
	root -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))'
	echo "Local analysis" >> .runhistory
	$(call upload_result,AnalysisResults,test-analysis-pp)
	$(call upload_result,TrackAverages,test-averages-pp)
	@make unlink || echo "Directory is clean"
	# make compare


clean:
	rm -f *.so *.d *~ Task*  *$(DATASET)*.root EventStat_temp.root test-analysis-pp.root event_stat.root



define jetjet
	$(foreach var,$(PtBins),$(call $(1),$(2)_$(var));)
endef


define gridstart
	root -l -b -q 'run.C("$(1)", "grid", "full", "$(DPART)", $(MC))' 
	rm -f *.xml .*xml
	echo "Started grid analysis on" "$(1)" >> .runhistory
	sleep $(PAUSE) 
endef


define terminatestart
	root -l -q 'run.C("$(1)", "grid", "terminate", "$(DPART)", $(MC))'
	echo "Terminated grid analysis" >> .runhistory	
endef

define downloadstart
	root -l -q 'run.C("$(1)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)'
	mv AnalysisResults.root $(1).root
	-root -l -q 'scaleBins.C("$(1).root", "$(1).root/PythiaInfoOnlyTender/")'
	@echo $(1) " Done."  
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
	-alien_cp -n $(1) alien:$(ALIEN_HOME)
endef


