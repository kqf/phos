include ../../base.mk

PROTONS_PATH=../../

DATASET = LHC16l-pass1
DPART = first
MC = kFALSE
OUTDIR = results/mc/pythia/debug_weights

# PROFILING_TARGET = root.exe -b -l -q 'run.C("$(DATASET)", "local", "test", "$(DPART)", $(MC))'
PROFILING_TARGET = root.exe -b -l -q playground.C+g
# PROFILING_TARGET = ./main
TEST_SELECTION = PhysTender


# profiling: | %.cxx
profiling:
	valgrind --tool=memcheck \
	--error-limit=no \
	--log-file=./profiling_result_long.log \
	--suppressions=${ROOTSYS}/etc/valgrind-root.supp \
	--max-stackframe=3060888 \
	--num-callers=40 \
	--show-leak-kinds=definite \
	--log-file=./profiling_result.log \
	--undef-value-errors=no \
	--leak-check=full \
	${PROFILING_TARGET}
	@$(call funlink) && echo "Directory is clean"

# Dirty?!? hack to avoid grid(plugin) limitations.
# Add all necessary taks
%.cxx:
	@$(call funlink)
	@$(call link_sources,../../tasks/analysis-task-pp/, "*.h" "*.cxx")

main: main.cc
	g++ main.cc -g -o main `root-config --cflags --libs` \
		-I./ \
		-isystem ${ALICE_ROOT} \
		-isystem ${ALICE_ROOT}/include \
		-isystem ${ALICE_PHYSICS} \
		-isystem ${ALICE_PHYSICS}/include \
		-isystem ${ALICE_PHYSICS}/PWGGA/PHOSTasks/PHOS_LHC16_pp/\
		-L${ALICE_ROOT}/lib \
		-L${ALICE_PHYSICS}/lib \
		-lESD -lAOD -lESDfilter -lSTEER -lANALYSISaliceBase -lANALYSIS -lANALYSISalice -lMFTbase -lAliHLTGlobal -lGPUTracking -lSTEERBase -lALIGN -lTPCbase -lTPCupgrade \
# 		-lPWGGAPHOSTasks
		# -lPWGGAUtils -lPWGCFfemtoscopy -lPWGflowTasks \

	./main
# 	rm main
# 		-lAliHLTJET -lCORRFW -lEventMixing -lFASTJETAN -lJETAN -lML -lOADB -lPWGCALO -lPWGCaloTrackCorrBase -lPWGCFChaoticity -lPWGCFCorrelationsBase -lPWGCFCorrelationsC2 -lPWGCFCorrelationsDPhi -lPWGCFCorrelationsEPCorrelation -lPWGCFCorrelationsJCORRANPro -lPWGCFCorrelationsJCORRAN -lPWGCFCorrelationsJFlowBase -lPWGCFCorrelationsThreePart -lPWGCFebye -lPWGCFEfficiencyTask -lPWGCFESE -lPWGCFFemtoDream -lPWGCFFEMTOSCOPYAOD -lPWGCFfemtoscopy -lPWGCFfemtoscopyUser -lPWGCFflowBW -lPWGCFflowCME -lPWGCFflowCMETwoPwrtRP -lPWGCFFlowForward -lPWGCFFLOWGF -lPWGCFHBTwrtEP -lPWGCFHCascadeAnalysis -lPWGCFK0Analysis -lPWGCFKPAnalysis -lPWGCFPLamAnalysisPP -lPWGCFunicor -lPWGCFV0LamAnalysis -lPWGCocktail -lPWGDevNanoAOD -lPWGDQbase -lPWGDQdielectron -lPWGDQreducedTree -lPWGEMCALbase -lPWGEMCALtasks -lPWGEMCALtriggerPart -lPWGEMCALtrigger -lPWGflowBase -lPWGflowTasks -lPWGGACaloTrackCorrelations -lPWGGAEMCALTasks -lPWGGAGammaConvBase -lPWGGAGammaConv -lPWGGAHyperon -lPWGGAPHOSTasks -lPWGGAUtils -lPWGGlauber -lPWGHFbase -lPWGHFcorrelationHF -lPWGHFhfe -lPWGHFHFMuFlow -lPWGHFjetsHF -lPWGHFtreeHF -lPWGHFvertexingHF -lPWGHMTF -lPWGJEEMCALJetTasks -lPWGJEFlavourJetTasks -lPWGJE -lPWGJEStrangenessInJets -lPWGJETFW -lPWGLFcommonutils -lPWGLFforward2 -lPWGLFnuclex -lPWGLFppvsmult -lPWGLFQATasks -lPWGLFresonances -lPWGLFrsnextra -lPWGLFspectraJET -lPWGLFspectra -lPWGLFSTRANGENESS -lPWGLFthermalfits -lPWGLFtotEt -lPWGmftmuondepCharmonium -lPWGMMMult -lPWGMMue -lPWGmuonaaf -lPWGmuondepaaf -lPWGmuondep -lPWGmuon -lPWGPPAlignment -lPWGPPEMCAL -lPWGPPevcharQnInterface -lPWGPPevcharQn -lPWGPPevchar -lPWGPPMUONdep -lPWGPPMUONlite -lPWGPPpid -lPWGPP -lPWGTools -lPWGTRD -lPWGUDbase -lPWGUDdiffractive -lPWGUDFP -lPWGUDselectors -lPWGUDupc -lRUN3 -lTender -lTenderSupplies -lvertexingHFTMVA -lvHFBDT
# 		-lPWGGAEMCALTasks -lPWGGAGammaConvBase -lPWGGAGammaConv -lPWGGAHyperon -lPWGGAPHOSTasks -lPWGGAUtils
