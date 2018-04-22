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
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();
	cuts_eta.fAsymmetryCut = 0.7;

	if (isTest || !isMC)
	{
		// TODO: Add plain selections
		AliPP13SelectionWeights & data_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kData);
		AliPP13SelectionWeights & data_weights_plain = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain);

		selections->Add(new AliPP13PhysPhotonSelection("Phys", "Physics Selection", cuts_pi0, &data_weights));
		// selections->Add(new AliPP13PhysPhotonSelection("PhysPlain", "Physics Selection no TOF cut efficiency", cuts_pi0, &data_weights_plain));
		// selections->Add(new AliPP13PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0, &data_weights));

		selections->Add(new AliPP13PhysPhotonSelection("Eta", "Physics Selection for eta meson", cuts_eta, &data_weights));
		// selections->Add(new AliPP13PhysPhotonSelection("EtaPlain", "Physics Selection for eta meson no TOF cut efficiency", cuts_eta, &data_weights_plain));
		// selections->Add(new AliPP13PhotonTimecutStudySelection("EtaTime", "Testing Timing Selection for eta meson", cuts_eta, &data_weights));

		// selections->Add(new AliPP13TagAndProbeSelection("TagAndProbleTOF", "Cluster p_{T} Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlinEst", "Physics efficiency for neutral particles", cuts_pi0, &data_weights));
		// selections->Add(new AliPP13NonlinearitySelection("PhysNonlinEstPlain", "Physics efficiency for neutral particles", cuts_pi0, &data_weights_plain));

		// selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster p_{T} Selection with timing cut", cuts_pi0, &data_weights, 10., 3.));

		selections->Add(new AliPP13PhotonSpectrumSelection("Photons", "Cluster p_{T} Selection", cuts_pi0, &data_weights));
		// selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsPlain", "Cluster p_{T} Selection", cuts_pi0, &data_weights_plain));

	}
	
	selections->Add(new AliPP13EpRatioSelection("EpRatio", "E/p ratio selection for electrons", cuts_pi0, &data_weights));

	if (isTest || isMC)
	{
		AliPP13SelectionWeightsMC & mc_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kMC);
		AliPP13SelectionWeightsMC & mc_weights_only = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kMC);

		// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
		// The pi^0 peak is misplaced in this fit: A * 1.03274e+00 (global energy scale)
		// Calculated for the updated version for the corrected Data
		mc_weights.fNonA = -0.020025549129372242;
		mc_weights.fNonSigma = 1.1154536660217529;
	    mc_weights.fNonGlobal = 1.0493128193171741;

		mc_weights_only.fNonGlobal = 1.0;
		mc_weights_only.fNonA = 0.0;

		selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));
		selections->Add(new AliPP13EfficiencySelectionMC("PhysEffPlain", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only));

		selections->Add(new AliPP13NonlinearitySelection("PhysNonlin", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights, kTRUE));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlinRaw", "Raw nonlinearity for neutral particles", cuts_pi0, &mc_weights_only, kTRUE));

		selections->Add(new AliPP13NonlinearityScanSelection("PhysNonlinScan", "Physics efficiency for neutral particles", cuts_pi0, &mc_weights));
		selections->Add(new AliPP13MesonSelectionMC("MCStudy", "MC Selection with timing cut", cuts_pi0, &mc_weights));
		selections->Add(new AliPP13KaonToPionRatioMC("KaonToPionRatio", "MC Selection for kaon/pion ratio", cuts_pi0, &mc_weights));
	}

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
