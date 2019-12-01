#include <iostream>
#include <TList.h>
#include <AliPP13SpectrumSelection.h>
#include <AliPP13PhotonTimecutStudySelection.h>
#include <AliPP13TagAndProbeSelection.h>
#include <AliPP13NonlinearitySelection.h>
#include <AliPP13QualityPhotonSelection.h>
#include <AliPP13PhotonSpectrumSelection.h>
#include <AliPP13EfficiencySelectionMC.h>
#include <AliPP13NonlinearitySelection.h>
#include <AliPP13NonlinearityScanSelection.h>
#include <AliPP13MesonSelectionMC.h>
#include <AliAnalysisTaskPP13.h>

using std::cerr;
using std::endl;
using std::cout;


void AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", Bool_t isMC = kFALSE, Bool_t isTest = kFALSE)
{
	// LoadAnalysisLibraries();
	
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
	cuts_eta.fAsymmetryCut = 0.7;

	if (isTest || !isMC)
	{
		// TODO: Add plain selections
		AliPP13SelectionWeights & data_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kData);
		AliPP13SelectionWeights & data_weights_plain = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kPlain);

		selections->Add(new AliPP13SpectrumSelection("Phys", "Physics Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13SpectrumSelection("PhysPlain", "Physics Selection no TOF cut efficiency", cuts_pi0, &data_weights_plain));
		selections->Add(new AliPP13PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0, &data_weights));

		selections->Add(new AliPP13SpectrumSelection("Eta", "Physics Selection for eta meson", cuts_eta, &data_weights));
		selections->Add(new AliPP13SpectrumSelection("EtaPlain", "Physics Selection for eta meson no TOF cut efficiency", cuts_eta, &data_weights_plain));
		selections->Add(new AliPP13PhotonTimecutStudySelection("EtaTime", "Testing Timing Selection for eta meson", cuts_eta, &data_weights));

		selections->Add(new AliPP13TagAndProbeSelection("TagAndProbleTOF", "Cluster p_{T} Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlin", "Physics efficiency for neutral particles", cuts_pi0, &data_weights));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlinPlain", "Physics efficiency for neutral particles", cuts_pi0, &data_weights_plain));

		selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster p_{T} Selection with timing cut", cuts_pi0, &data_weights, 10., 3.));
		
		selections->Add(new AliPP13PhotonSpectrumSelection("Photons", "Cluster p_{T} Selection", cuts_pi0, &data_weights));
		selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsPlain", "Cluster p_{T} Selection", cuts_pi0, &data_weights_plain));

		delete &data_weights;
		delete &data_weights_plain;
	}	


	if (isTest || isMC)
	{
		AliPP13SelectionWeightsMC & mc_weights = dynamic_cast<AliPP13SelectionWeightsMC &>(
			AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kMC)
		);
		AliPP13SelectionWeightsMC & mc_weights_only = dynamic_cast<AliPP13SelectionWeightsMC &>(
			AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kMC)
		);


		// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
		// The pi^0 peak is misplaced in this fit: A * 1.03274e+00 (global energy scale)
		// Calculated for the updated version for the corrected Data

		selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles fully corrected", cuts_pi0, &mc_weights));
		selections->Add(new AliPP13EfficiencySelectionMC("PhysEffPlain", "Physics efficiency for neutral particles, no nonlinearity", cuts_pi0, &mc_weights_only));

		selections->Add(new AliPP13NonlinearitySelection("PhysNonlin", "Physics nonlinearity for neutral particles", cuts_pi0, &mc_weights, kTRUE));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlinRaw", "Raw nonlinearity for neutral particles", cuts_pi0, &mc_weights_only, kTRUE));

		selections->Add(new AliPP13NonlinearityScanSelection("PhysNonlinScan", "Physics efficiency for neutral particles", cuts_pi0, &mc_weights));
		selections->Add(new AliPP13MesonSelectionMC("MCStudy", "MC Selection with timing cut", cuts_pi0, &mc_weights));	

		delete & mc_weights;
		delete & mc_weights_only;
	}

	// Setup task
	AliAnalysisTaskPP13 * task = new AliAnalysisTaskPP13("PhosProtons", selections);
	task->SelectCollisionCandidates(offlineTriggerMask);
	mgr->AddTask(task);
	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (Int_t i = 0; i < task->GetSelections()->GetEntries(); ++ i)
	{
		AliPP13PhysicsSelection * fSel = dynamic_cast<AliPP13PhysicsSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		std::cout << fSel->GetTitle() << std::endl;

		coutput = mgr->CreateContainer(fSel->GetName() + suff,
		                               TList::Class(),
		                               AliAnalysisManager::kOutputContainer,
		                               AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}
}
