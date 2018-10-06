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

	// Applying no weights
	//
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	cuts_pi0.fTimingCut = 1000e-9;

	// TODO: Add plain selections
	AliPP13SelectionWeights & data_weights_plain = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain);

	TList * selections = new TList();
	selections->Add(new AliPP13SpectrumSelection("Phys", "Physics Selection", cuts_pi0, &data_weights_plain));
	selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0, &data_weights_plain));
	selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster p_{T} Selection with timing cut", cuts_pi0, &data_weights_plain, 10., 3.));

	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);
	task->SelectCollisionCandidates(offlineTriggerMask);
	mgr->AddTask(task);
	mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	cout << "ADDING A NEW TASK" << endl;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhysicsSelection * fSel = dynamic_cast<AliPP13PhysicsSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		cout << "Selection " << fSel->GetName() << " " << i << endl;
		coutput = mgr->CreateContainer(fSel->GetName() + suff,
									   TList::Class(),
									   AliAnalysisManager::kOutputContainer,
									   AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
	cout << "ADDED A NEW TASK" << endl;
}
