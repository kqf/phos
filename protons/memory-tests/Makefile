DATASET = LHC16i-muon-calo-pass1
DPART = second
MC = kFALSE
PROFILING_TARGET = 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))'

TEST_SELECTION = PhysTender

profiling: | %.cxx
	valgrind --tool=memcheck \
	--error-limit=no \
	--max-stackframe=3060888 \
	--suppressions=${ROOTSYS}/etc/valgrind-root.supp \
	--num-callers=40 \
	--log-file=./profiling_result.log \
	${PROFILING_TARGET}


%.cxx:
	@$(call funlink)	
	@# Dirty?!? hack to avoid grid(plugin) limitations.
	@# Add all necessary taks
	@$(call link_sources,../../qa/qa-task,AddTaskCaloCellsQAPt.C "*.h")
	@$(call link_sources,../analysis-task-pp, "*.h" "*.cxx")
	@$(call link_sources,../../qa/qa-track-averages,AddAnalysisTaskTrackAverages.C "*.h" "*.cxx")


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
	rm *.so *.d *~ Task*

unlink:
	$(call funlink) 	

	
define funlink
	find -type l -delete	
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

