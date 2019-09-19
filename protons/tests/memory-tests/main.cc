#include <TList.h>
#include <TSystem.h>
#include <AliAnalysisManager.h>
#include <AliPIDResponseInputHandler.h>
#include <AliMultiInputEventHandler.h>
#include <AliAnalysisTaskPIDResponse.h>
#include <AliVParticle.h>
#include "AliFlowTrackSimpleCuts.h"
#include <AliDalitzAODESD.h>
#include <AliAODInputHandler.h>
#include <AliAnalysisTaskPP13.h>
#include <AliPP13PhysicsSelection.h>
#include <AliPP13ClusterCuts.h>
#include <AliPP13SelectionWeights.h>
#include <AliPP13SpectrumSelectionSimple.h>

#include "plugin.h"
// #include <maintask.h>

// #include <ANALYSIS/macros/AddTaskPIDResponse.C>
// #include <OADB/macros/AddTaskPhysicsSelection.C>
// #include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
// #include <PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C>
// #include <AliPP13TriggerProperties.h>
AliAnalysisTaskPP13 * AddSimpleAnalysisTaskPP(
	Bool_t isMC = kFALSE,
	TString description = "",
	TString suff = ""
)
{
	// Setup Analysis Selections
	//
	TList * selections = new TList();

	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();
	cuts_eta.fAsymmetryCut = 0.7;


	AliPP13SelectionWeights & data_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kData);

	selections->Add(new AliPP13SpectrumSelectionSimple("SimplePhys", "Physics Selection", cuts_pi0, &data_weights));
	selections->Add(new AliPP13SpectrumSelectionSimple("SimpleEta", "Physics Selection for eta meson", cuts_eta, &data_weights));

	delete &data_weights;

	// Setup the main task
	//
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);

	AliAnalysisManager * manager = AliAnalysisManager::GetAnalysisManager();
	manager->AddTask(task);
	manager->ConnectInput(task, 0, manager->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhysicsSelection * fSel = dynamic_cast<AliPP13PhysicsSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		coutput = manager->CreateContainer(
			fSel->GetName() + suff,
			TList::Class(),
			AliAnalysisManager::kOutputContainer,
			AliAnalysisManager::GetCommonFileName()
		);

		manager->ConnectOutput(task, i + 1, coutput);
	}
	return task;
}


int main()
{
	TString period = "LHC16l-pass1";
	const char * runmode = "local";
	const char * pluginmode = "test";
	TString dpart = "first";
	Bool_t isMC = kFALSE;
	Bool_t useJDL = kTRUE;

    // AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    // manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL, isMC));
    // manager->SetInputEventHandler(new AliAODInputHandler());

	// AliAnalysisTaskPP13 *physseltask = reinterpret_cast<AliAnalysisTaskPP13 *>(gInterpreter->ProcessLine(Form(".x %s", gSystem->ExpandPathName("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_LHC16_pp/macros/AddAnalysisTaskPP.C"))));
}
