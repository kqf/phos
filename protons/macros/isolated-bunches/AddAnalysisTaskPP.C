#include "../../setup/sources.h"

void AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "", const std::vector<Int_t>  & v, Bool_t isMC = kFALSE, Bool_t isTest = kFALSE)
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
	cuts_pi0.fTimingCut = 1000e-9;

	// TODO: Add plain selections
	AliPP13SelectionWeights & data_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kData);
	AliPP13SelectionWeights & data_weights_plain = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain);

	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);

	if ( !badmap.IsNull() )
		task->SetBadMap(badmap);

	if (v.size() > 0)
	{
		const Int_t nexc = v.size();
		Int_t excells[nexc];
		for (int i = 0; i < v.size(); ++i)
			excells[i] = v[i];

		task->SetBadCells(excells, nexc);
	}

	if (v.size() > 0 && !badmap.IsNull())
		cout << "Warning, you are setting bad cells and bad map! Be sure that you know what you are doing" << endl;

	// task->GetSelections()->Add
	task->SelectCollisionCandidates(offlineTriggerMask);
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
}
