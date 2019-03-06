include ../../base.mk

DATASET = LHC16i-muon-calo-pass1
DPART = second
MC = kFALSE
OUTDIR = results/data/corrected/

#DATASET = LHC17d20a2_extra
#DPART = second
#MC = kTRUE
#OUTDIR = results/mc/pythia

TEST_SELECTION = PhysTender

%.cxx:
	@$(call funlink)	
	@# Dirty?!? hack to avoid grid(plugin) limitations.
	@# Add all necessary taks
	@$(call link_sources,../phys-qa/macros,AddTaskCaloCellsPhysQA.C)
	@$(call link_sources,../phys-qa/macros,AddTaskPhysPHOSQA.C "*.h")
	@$(call link_sources,../phys-qa, "*.h" "*.cxx")
