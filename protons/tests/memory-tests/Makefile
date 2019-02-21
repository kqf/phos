include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16k-pass1
DPART = first
MC = kFALSE
OUTDIR = results/mc/pythia/debug_weights

PROFILING_TARGET = root -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))'
TEST_SELECTION = PhysTender

# profiling: | %.cxx
profiling:
	valgrind --tool=memcheck \
	--error-limit=no \
	--max-stackframe=3060888 \
	--num-callers=40 \
	--log-file=./profiling_result.log \
	--leak-check=full \
	--track-origins=yes \
	--show-reachable=yes \
	${PROFILING_TARGET}
	@$(call funlink) && echo "Directory is clean"

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
