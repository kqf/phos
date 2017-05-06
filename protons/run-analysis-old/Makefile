DATASET = LHC15g6b
DPART = first
MC = kTRUE

grid: | %.cxx
	$(call gridstart,$(DATASET)) || make unlink
	@make unlink || echo "Directory is clean"

terminate: | %.cxx
	$(call terminatestart,$(DATASET))
	@make unlink || echo "Directory is clean"

download: | %.cxx
	$(call downloadstart,$(DATASET))
	@make unlink || echo "Directory is clean"

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

upload:
	$(call upload_result,AnalysisResults,$(DATASET))
	# $(call upload_result,TrackAverages,TrackAverages.$(DATASET))

clean:
	rm *.so *.d *~ Task*


gridjetjet: | %.cxx
	$(call jetjet,gridstart,$(DATASET)) || make unlink
	@make unlink || echo "Directory is clean"

terminatejetjet: | %.cxx
	$(call jetjet,terminatestart,$(DATASET)) || make unlink
	@make unlink || echo "Directory is clean"

downloadjetjet: | %.cxx
	$(call jetjet,downloadstart,$(DATASET)) || make unlink
	@make unlink || echo "Directory is clean"



PtBins = 20
define jetjet
	$(foreach var,$(PtBins),$(call $(1),$(2)_$(var));)
endef

define gridstart
	root -l -b -q 'run.C("$(1)", "grid", "full", "$(DPART)", $(MC))' 
	echo "Started grid analysis on" "$(1)" >> .runhistory
endef


define terminatestart
	root -l -q 'run.C("$(1)", "grid", "terminate", "$(DPART)", $(MC))'
	echo "Terminated grid analysis" >> .runhistory	
endef

define downloadstart
	root -l -q 'run.C("$(1)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)'
	$(call upload_result,AnalysisResults,$(1))
	echo "Terminated grid analysis" >> .runhistory
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
	-alien_cp -n $(2).root alien:$(ALIEN_HOME)
endef


