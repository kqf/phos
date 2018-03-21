include ../../base.mk

DATASET = LHC17d20a2_extrassss
DPART = first
MC = kTRUE
OUTDIR = results/mc/pythia

TEST_SELECTION = PhysTender

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
