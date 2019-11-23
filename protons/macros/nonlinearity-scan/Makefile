include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Run final efficiency fine nonlinearity binning
#
DATASET = LHC17j3b1
OUTDIR = results/mc/single/pi0/extended_pt_range_1
TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@echo "Start"
# 	@$(call funlink)
# 	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
