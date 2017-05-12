PROFILING_TARGET = root -l -q 'run.C("local", "test")'
RESULTS = LHC16k-MyTask
DPART = second
MC = kFALSE


caf:
	root -l RunPoD.C
	# root -l -q RunPoD.C
	
grid:
	root -l -b -q 'run.C("$(DATASET)", "grid", "full", "$(DPART)", $(MC))' 	
	echo "Started grid analysis" >> .runhistory
	@echo -e "\x07"

merge:
	root -l -b -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC))' 	
	mv AnalysisResults.root $(RESULTS).root
	echo "Terminated grid analysis" >> .runhistory
	@echo -e "\x07"

download:
	root -l -b -q 'run.C("$(DATASET)", "grid", "terminate", "$(DPART)", $(MC), kFALSE)' 	
	mv AnalysisResults.root $(RESULTS).root
	echo "Downloaded files analysis" >> .runhistory
	@echo -e "\x07"

test:
	root -l -q 'run.C("local", "test", $(MC))'
	echo "Local analysis" >> .runhistory
	-./dumpres.py 2> /dev/null

	@# Rename and move the results
	@mv AnalysisResults.root test-pp-task.root
	-./compare-results.py test-pp-task.root
	alien_cp -n test-pp-task.root alien:$(ALIEN_HOME)
	@echo -e "\x07"

clean:
	rm *.so *.d *~ Task*


compare:
	./compare-results.py 2> /dev/null

profiling:
	valgrind --tool=memcheck \
	--error-limit=no \
	--max-stackframe=3060888 \
	--suppressions=${ROOTSYS}/etc/valgrind-root.supp \
	--num-callers=40 \
	--log-file=./profiling_result.log \
	${PROFILING_TARGET}


# --leak-check=full \
