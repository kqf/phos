include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Finetune the global energy scale High
#
DATASET = LHC17j3b1
OUTDIR = results/mc/single/pi0/debug10
TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/debug/, "*.h" "*.cxx")
