PROFILING_TARGET = root -l -q 'run.C("local", "test")'

test:
	root -l -q 'run.C("local", "test")'
	echo "Local analysis" >> .runhistory
	# make compare

grid:
	root -l -b -q 'run.C("grid", "full")'
	echo "Started grid analysis" >> .runhistory

terminate:
	root -l -q 'run.C("grid", "terminate")'
	echo "Terminated grid analysis" >> .runhistory


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
