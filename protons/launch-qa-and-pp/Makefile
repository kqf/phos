DATASET = LHC16o-muon-calo-pass1

grid: | %.cxx
	root -l -b -q 'run.C("$(DATASET)", "grid", "full")' || make unlink 
	@make unlink || echo "Directory is clean"
	echo "Started grid analysis" >> .runhistory

%.cxx:
	make unlink
	@# Dirty?!? hack to avoid grid(plugin) limitations.
	@# Add all necessary taks
	$(call link_sources,../../qa/qa-task,AddTaskCaloCellsQAPt.C)
	ln -s ../analysis-task-pp/*.cxx .
	$(call link_sources,../analysis-task-pp,AddAnalysisTaskPP.C)
	$(call link_sources,../../qa/qa-track-averages,AddAnalysisTaskTrackAverages.C)

unlink:
	find -type l -delete

terminate: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate")' || make unlink
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory

download: | %.cxx
	root -l -q 'run.C("$(DATASET)", "grid", "terminate", kFALSE, kFALSE)' || make unlink
	mv AnalysisResults.root $(DATASET).root 
	-alien_cp -n $(DATASET).root alien:$(ALIEN_HOME)
	-alien_cp -n TrackAverages.root alien:$(ALIEN_HOME)
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory

# Ignore problems with ALICE::RRC-KI::SE
force-download:
	mkdir -p tmp 
	rm -rf LHC16o.root
	$(call save_runs,/alice/cern.ch/user/o/okovalen/phosqa-lhc16o-muon-calo-pass1-2gev-test,AnalysisResults.root,tmp)
	hadd LHC16o.root tmp/*.root
	rm -rf tmp 
	echo -e "\x07

test: | %.cxx
	root -l -q 'run.C("$(DATASET)", "local", "test")'
	echo "Local analysis" >> .runhistory
	@make unlink || echo "Directory is clean"
	# make compare

clean:
	rm *.so *.d *~ Task*

# output direcotry, filename.root, where to save
define save_runs
	for run in $$(alien_ls $(1)/output | grep .[0-9]*); do \
		alien_cp alien://$(1)/output/$$run/$(2) $(3)/$$run.root; \
	done	
endef


define link_sources
	ln -s $(1)/*.h .
	ln -s $(1)/$(2) .
endef

