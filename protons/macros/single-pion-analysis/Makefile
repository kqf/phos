include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Run final efficiency for optimized GE scale
#
DATASET = LHC17j3b1
OUTDIR = results/mc/single/pi0/scan_nonlinearities7
TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
