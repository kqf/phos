include ../../base.mk

#  >>>>>>>>  Don't change this <<<<<<<<<<<<
DPART = first
MC = kTRUE
PROTONS_PATH=../../
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# Run the analysis on the newest nonlinearity function
#
DATASET = LHC17j3c2
OUTDIR = results/mc/single/eta/acceptance_1
# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
