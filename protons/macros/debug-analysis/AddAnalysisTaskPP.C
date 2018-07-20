#include "../../tasks/debug/macros/sources.h"

void AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "")
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
	ClusterCuts cuts_pi0 = ClusterCuts::GetClusterCuts();
	ClusterCuts cuts_eta = ClusterCuts::GetClusterCuts();

	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	// Iteration d0
	SelectionWeights & mc_weights = SelectionWeights::Init(SelectionWeights::kSinglePi0MC);
	SelectionWeights & mc_weights_only = SelectionWeights::Init(SelectionWeights::kSinglePi0MC);
	mc_weights.fNonGlobal = 1.022;
	selections->Add(new EfficiencySelection("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));

	// Setup task
	AnalysisTaskDebug * task = new AnalysisTaskDebug("PhosProtons", selections);
	mgr->AddTask(task);



	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		PhotonSelection * fSel = dynamic_cast<PhotonSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		coutput = mgr->CreateContainer(fSel->GetName() + suff,
									   TList::Class(),
									   AliAnalysisManager::kOutputContainer,
									   AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
}