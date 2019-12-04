#include "../../setup/sources.h"

AliAnalysisTaskPP13 * AddAnalysisTaskPP(TString description, TString period)
{
	LoadAnalysisLibraries();

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
		throw "Fatal: There is no analysis manager";

	// Applying no weights
	//
	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();

	if (period.Contains("LHC16l") || period.Contains("LHC16o"))
	{
		cout << "Analyzing LHC16o or LHC16l" << endl;
		cuts_pi0.fTimingCut = 1250e-9;
	}
	else if (period.Contains("LHC16h"))
	{
		cout << "Analyzing LHC16h" << endl;
		cuts_pi0.fTimingCut = 500e-9;
	}
	else
	{
		throw "Doesn't work";
	}

	AliPP13SelectionWeights & data_weights_plain = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain);

	TList * selections = new TList();
	selections->Add(new AliPP13SpectrumSelection("Phys", "Physics Selection", cuts_pi0, &data_weights_plain));
	selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0, &data_weights_plain));
	selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster p_{T} Selection with timing cut", cuts_pi0, &data_weights_plain, 10., 3.));

	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);
	mgr->AddTask(task);
	mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhysicsSelection * fSel = dynamic_cast<AliPP13PhysicsSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		cout << "Selection " << fSel->GetName() << " " << i << endl;
		AliAnalysisDataContainer * coutput = mgr->CreateContainer(
		        fSel->GetName(),
		        TList::Class(),
		        AliAnalysisManager::kOutputContainer,
		        AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
	return task;
}
