
grid: | *.cxx
	root -l -b -q 'run.C("grid", "full")' || make unlink 
	@make unlink || echo "Directory is clean"
	echo "Started grid analysis" >> .runhistory

*.cxx:
	@# Dirty?!? hack to avoid grid(plugin) limitations.

	ln -s ../../qa/qa-task/*.cxx .
	ln -s ../../qa/qa-task/*.h .
	ln -s ../../qa/qa-task/AddTaskCaloCellsQAPt.C .

	ln -s ../analysis-task-pp/*.cxx .
	ln -s ../analysis-task-pp/*.h .
	ln -s ../analysis-task-pp/AddAnalysisTaskPP.C .

unlink:
	find -type l -delete


terminate: | *.cxx
	root -l -q 'run.C("grid", "terminate")' || make unlink
	@make unlink || echo "Directory is clean"
	echo "Terminated grid analysis" >> .runhistory


test:
	root -l -q 'run.C("local", "test")'
	echo "Local analysis" >> .runhistory
	# make compare

clean:
	rm *.so *.d *~ Task*