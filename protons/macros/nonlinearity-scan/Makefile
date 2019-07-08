include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Run final efficiency for optimized GE scale
#
DATASET = LHC17j3b1
OUTDIR = results/mc/single/pi0/final_nonlinearity_scan_3
TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@echo "Start"
# 	@$(call funlink)
# 	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
