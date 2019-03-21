#include "../../setup/sources.h"

AliAnalysisTaskPP13 * AddAnalysisTaskPP(TString description, TString suff = "")
{
	LoadAnalysisLibraries();
	
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
	{
		cerr << "Fatal: There is no analysis manager" << endl;
		return;
	}
	// Setup Selections
	TList * selections = new TList();

	// Applying no weights
	//
	AliPP13SelectionWeights data_weights;
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();
	cuts_eta.fAsymmetryCut = 0.7;
	selections->Add(new AliPP13EpRatioSelection("EpRatio", "E/p ratio selection for electrons", cuts_pi0, &data_weights));

	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);
	mgr->AddTask(task);
	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhysicsSelection * fSel = dynamic_cast<AliPP13PhysicsSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		coutput = mgr->CreateContainer(fSel->GetName() + suff,
									   TList::Class(),
									   AliAnalysisManager::kOutputContainer,
									   AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
	return task
}
