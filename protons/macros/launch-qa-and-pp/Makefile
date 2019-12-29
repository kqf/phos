include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16l-pass1
DPART = first
MC = kFALSE
# Use the same nonlinearity version for the both productions
#
OUTDIR = results/data/LHC16/no_physics_selection_test1
ALICE_SITE =


TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
