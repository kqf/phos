include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kFALSE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Run final efficiency for optimized GE scale
#
DATASET = LHC16g-pass1
OUTDIR = results/data/LHC16/trigger_qa/iteration3_kphi7/
TEST_SELECTION = PhysTender
OUTFILE = TriggerQA

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/trigger-qa/, "*.h" "*.cxx")
