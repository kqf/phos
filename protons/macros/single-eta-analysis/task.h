#include "../../setup/sources.h"

AliAnalysisTaskPP13 * AddAnalysisTaskPP(TString description, Bool_t acceptance=kFALSE)
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
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();

	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	AliPP13SelectionWeightsMC & mc_weights = dynamic_cast<AliPP13SelectionWeightsMC &>(
		AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSingleEtaMC)
	);

	AliPP13SelectionWeights & no_weights = dynamic_cast<AliPP13SelectionWeights &>(
		AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain)
	);

	mc_weights.fNonGlobal = -1.0; // Enable the cuts

	// NB: Don't use all other selections as they are not needed for the analysis
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_eta, &mc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEffNoA", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("NoWeights", "Physics efficiency no corrections", cuts_eta, &no_weights));

	if(acceptance){
		Int_t scale = 1;
		Int_t minDistanceMaximum = 4;
		for (Int_t i = 0; i < minDistanceMaximum; ++i)
		{

			AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
			cuts_pi0.fNContributors = 0;
			cuts_pi0.fMinimalDistance = i * scale;

			AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();
			cuts_eta.fNContributors = 0;
			cuts_eta.fAsymmetryCut = 0.7;
			cuts_eta.fMinimalDistance = i * scale;

			// TODO: Add plain selections
			selections->Add(new AliPP13EfficiencySelectionMC(Form("PhysEff%d", i), "Physics Selection", cuts_pi0, &mc_weights));
			selections->Add(new AliPP13EfficiencySelectionMC(Form("PhysEffEta%d", i), "Physics Selection for eta meson", cuts_eta, &mc_weights));
		}
	}
	delete &mc_weights;
	delete &no_weights;

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
