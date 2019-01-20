include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16l-pass1
DPART = first
MC = kFALSE
OUTDIR = results/mc/pythia/debug_weights


TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
