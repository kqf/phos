#include "../setup/sources.h"

void AddAnalysisTaskPP(TString description, TString suff = "", TString badmap = "", const std::vector<Int_t>  & v)
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

	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();

	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	AliPP13SelectionWeightsMC & spmc_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSingleEtaMC);
	AliPP13SelectionWeightsMC & spmc_weights_only = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSingleEtaMC);
	spmc_weights_only.fNonGlobal = 1.0;
	spmc_weights_only.fNonA = 0.0;

	// NB: Don't use all other parametrizations as they are not needed for the analysis
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_eta, &spmc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEffNoA", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &spmc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEffPlain", "Physics efficiency for neutral particles, no nonlinearity", cuts_eta, &spmc_weights_only));

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

	// Don't use collision candidats for single particle productions
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
