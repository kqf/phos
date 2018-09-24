include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16l-muon-calo-pass1
DPART = first
MC = kFALSE
OUTDIR = results/data/new-calibration

#DATASET = LHC17d20a1_extra
#DPART = first
#MC = kTRUE
#OUTDIR = results/mc/pythia

TEST_SELECTION = PhysTender
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")
