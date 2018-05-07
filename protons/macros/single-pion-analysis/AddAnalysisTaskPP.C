#include "../../setup/sources.h"

void AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "")
{
	Int_t id = gClassTable->GetID("AliAnalysisTaskPP13");
	// Load analysis libraries for the older versions of aliphysics
	// without the task being manually added
	if(id == -1)
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
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();

	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	// Iteration d0
	AliPP13SelectionWeightsSPMC & mc_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
	AliPP13SelectionWeightsSPMC & mc_weights_only = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);

	mc_weights_only.fNonGlobal = 1.0;
	mc_weights_only.fNonA = 0.0;
	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));
	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEffPlain", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlin", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights, kTRUE));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlinPlain", "Plain nonlinearity for neutral particles", cuts_pi0, &mc_weights_only, kTRUE));


	// Iteration d1
	AliPP13SelectionWeightsSPMC & mc_weights1 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
	AliPP13SelectionWeightsSPMC & mc_weights_only1 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
    mc_weights1.fW0 = 1.4424726043375593;
    mc_weights1.fW1 = 0.15126295815022361;
    mc_weights1.fW2 = 8.108172429708121;

	mc_weights_only1.fNonGlobal = 1.0;
	mc_weights_only1.fNonA = 0.0;
    mc_weights_only1.fW0 = 1.4424726043375593;
    mc_weights_only1.fW1 = 0.15126295815022361;
    mc_weights_only1.fW2 = 8.108172429708121;

	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEff1", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights1));
	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEffPlain1", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only1));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlin1", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights1, kTRUE));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlinPlain1", "Plain nonlinearity for neutral particles", cuts_pi0, &mc_weights_only1, kTRUE));


	// Iteration d2
	AliPP13SelectionWeightsSPMC & mc_weights2 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
	AliPP13SelectionWeightsSPMC & mc_weights_only2 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);

    mc_weights2.fW0 = 1.5502651563423713;
    mc_weights2.fW1 = 0.1501143223817212;
    mc_weights2.fW2 = 8.156749093659146;

	mc_weights_only2.fNonGlobal = 1.0;
	mc_weights_only2.fNonA = 0.0;
    mc_weights_only2.fW0 = 1.5502651563423713;
    mc_weights_only2.fW1 = 0.1501143223817212;
    mc_weights_only2.fW2 = 8.156749093659146;

	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEff2", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights2));
	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEffPlain2", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only2));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlin2", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights2, kTRUE));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlinPlain2", "Plain nonlinearity for neutral particles", cuts_pi0, &mc_weights_only2, kTRUE));

	// Iteration d3 (estimated from 0 < pT < 10 interval)
	AliPP13SelectionWeightsSPMC & mc_weights3 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
	AliPP13SelectionWeightsSPMC & mc_weights_only3 = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);

    mc_weights3.fW0 = 1.490487117730805;
    mc_weights3.fW1 = 0.15303013222262335;
    mc_weights3.fW2 = 8.241894695494016;

	mc_weights_only3.fNonGlobal = 1.0;
	mc_weights_only3.fNonA = 0.0;
    mc_weights_only3.fW0 = 1.490487117730805;
    mc_weights_only3.fW1 = 0.15303013222262335;
    mc_weights_only3.fW2 = 8.241894695494016;

	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEff3", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights3));
	selections->Add(new AliPP13EfficiencySelectionSPMC("PhysEffPlain3", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only3));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlin3", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights3, kTRUE));
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlinPlain3", "Plain nonlinearity for neutral particles", cuts_pi0, &mc_weights_only3, kTRUE));


	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);

	// Don't set map of bad channels on task level.
	// Always apply tender
	// if ( !badmap.IsNull() )
	// 	task->SetBadMap(badmap);

	// task->GetSelections()->Add
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
