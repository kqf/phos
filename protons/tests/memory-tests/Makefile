include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16k-pass1
DPART = first
MC = kFALSE
OUTDIR = results/mc/pythia/debug_weights

PROFILING_TARGET = root -b -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))'
TEST_SELECTION = PhysTender


# profiling: | %.cxx
profiling:
	valgrind --tool=massif \
	--error-limit=no \
	--num-callers=40 \
	--log-file=./profiling_result.log \
	--suppressions=${ROOTSYS}/etc/valgrind-root.supp \
	${PROFILING_TARGET}
	@$(call funlink) && echo "Directory is clean"

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")

main: main.cc
	g++ main.cc -g -o main `root-config --cflags --libs` \
		-I./ \
		-I${ALICE_ROOT} \
		-I${ALICE_ROOT}/include \
		-I${ALICE_PHYSICS} \
		-I${ALICE_PHYSICS}/include \
		-I${ALICE_PHYSICS}/PWGGA/PHOSTasks/PHOS_LHC16_pp/\
		-L${ALICE_ROOT}/lib \
		-L${ALICE_PHYSICS}/lib
	# rm main
