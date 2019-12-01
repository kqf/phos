#include "../../setup/sources.h"

AliAnalysisTaskPP13 * AddAnalysisTaskPP(TString description, Bool_t calculate_acceptance = kFALSE)
{
	// LoadAnalysisLibraries();

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
	{
		throw "Fatal: There is no analysis manager";
	}
	// Setup Selections
	TList * selections = new TList();

	// Applying no weights
	//
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	cuts_pi0.fNContributors = 0;

	AliPP13SelectionWeightsMC & mc_weights = dynamic_cast<AliPP13SelectionWeightsMC &>(
		AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC)
	);
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));

	AliPP13SelectionWeightsMC & scan_weights = dynamic_cast<AliPP13SelectionWeightsScan &>(
		AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kScan)
	);

	Float_t precA = nsigma * 0.0005 * 2 / nbins * scan_weights.fE;
	Float_t precD = nsigma * 0.0002 * 2 / nbins * scan_weights.fD;
	selections->Add(new AliPP13NonlinearityScanSelection("PhysNonlinScan", "Physics efficiency for neutral particles", cuts_pi0, &scan_weights, precA, precSigma));

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

		coutput = mgr->CreateContainer(fSel->GetName(),
									   TList::Class(),
									   AliAnalysisManager::kOutputContainer,
									   AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
	return task;
}
