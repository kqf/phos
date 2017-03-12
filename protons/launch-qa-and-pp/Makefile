DATASET = LHC16k-pass1

grid: | %.cxx
	root -l -b -q 'run.C("$(DATASET)", "grid", "full")' || make unlink 
	@make unlink || echo "Directory is clean"
	echo "Started grid analysis" >> .runhistory

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
	root -l -q 'run.C("$(DATASET)", "grid", "terminate")' || make unlink
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory

download: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", kFALSE, kFALSE)' || make unlink
	make upload
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	mkdir -p tmp 
	rm -rf LHC16o.root
	$(call save_runs,$(ALIEN_HOME)/pp-phos-$(DATASET),AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	rm -rf tmp 
	echo -e "\x07

test: | %.cxx
	root -l -q 'run.C("$(DATASET)", "local", "test")'
	echo "Local analysis" >> .runhistory
	$(call upload_result,AnalysisResults,test-analysis-pp)
	$(call upload_result,TrackAverages,test-averages-pp)
	@make unlink || echo "Directory is clean"
	# make compare

upload:
	$(call upload_result,AnalysisResults,$(DATASET))
	$(call upload_result,TrackAverages,TrackAverages.$(DATASET))

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


