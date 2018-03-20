#include "../setup/sources.h"

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
	AliPP13SelectionWeights data_weights;
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();
	
	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	AliPP13SelectionWeightsMC & mc_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSingleEtaMC);
	AliPP13SelectionWeightsMC & mc_weights_only = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSingleEtaMC);


	mc_weights_only.fNonGlobal = 1.0;
	mc_weights_only.fNonA = 0.0;

	// NB: Don't use all other selections as they are not needed for the analysis
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_eta, &mc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEffNoA", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEffPlain", "Physics efficiency for neutral particles, no nonlinearity", cuts_eta, &mc_weights_only));


	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);

	if ( !badmap.IsNull() ) 
		task->SetBadMap(badmap);

	// task->SelectCollisionCandidates(offlineTriggerMask);
	mgr->AddTask(task);



	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhotonSelection * fSel = dynamic_cast<AliPP13PhotonSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		coutput = mgr->CreateContainer(fSel->GetName() + suff,
		                               TList::Class(),
		                               AliAnalysisManager::kOutputContainer,
		                               AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
}
