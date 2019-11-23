include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Run the analysis with the correct nonlinearity function
#
DATASET = LHC17j3c1
OUTDIR = results/mc/single/pi0/extended_pt_range_2
TEST_SELECTION = PhysEff
# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@echo "Doing nothing"
# 	@$(call funlink)
# 	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
