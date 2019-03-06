include ../../../base.mk

PROTONS_PATH=../../../

DATASET = LHC16g-muon-calo-pass1
DPART = first
MC = kFALSE

# DATASET = LHC17d20a1
# DPART = second
# MC = kTRUE

TEST_SELECTION = PhysTender

%.cxx:
	@$(call funlink)	
	@$(call link_sources,../analysis-task-pp, "*.h" "*.cxx")
	ln -s ../analysis-task-pp/macros/AddAnalysisTaskPP.C .
