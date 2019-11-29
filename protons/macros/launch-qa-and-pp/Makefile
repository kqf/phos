include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16g-pass1
DPART = first
MC = kFALSE
OUTDIR = results/data/LHC17/debug_tender_lhc16g
ALICE_SITE =


TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
