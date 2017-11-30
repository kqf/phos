#include "../loadlibraries.h"

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

	if (!isTest && !isMC)
	{
		selections->Add(new AliPP13PhysPhotonSelection("Phys", "Physics Selection", cuts_pi0));
		selections->Add(new AliPP13PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0));
		selections->Add(new AliPP13TagAndProbeSelection("TagAndProbleTOF", "Cluster P_{t} Selection", cuts_pi0));

		selections->Add(new AliPP13PhysPhotonSelection("Eta", "Physics Selection for eta meson", cuts_eta));
		selections->Add(new AliPP13PhotonTimecutStudySelection("EtaTime", "Testing Timing Selection for eta meson", cuts_eta));
		
		selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0));
		selections->Add(new AliPP13PhotonSpectrumSelection("Photons", "Cluster P_{t} Selection", cuts_pi0));
		selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster P_{t} Selection with timing cut", cuts_pi0, 10., 3.));
		selections->Add(new AliPP13NonlinearitySelection("PhysNonlinEst", "Physics efficiency for neutral particles", cuts_pi0, data_weights));
	}	

	// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
	// The pi^0 peak is misplaced in this fit: A * 1.03274e+00 (global energy scale)
	// Calculated for the updated version for the corrected Data
	Float_t nonlin_a = -0.020025549129372242;
	Float_t nonlin_b = 1.1154536660217529;
    Float_t ge_scale = 1.0493128193171741;

    Float_t weigh_a = -1.063;
    Float_t weigh_b = 0.855;
	
	if(isTest)
	{
		selections->Add(new AliPP13PhysPhotonSelection("Phys", "Physics Selection", cuts_pi0));
		selections->Add(new AliPP13PhotonSpectrumSelection("PhotonsTime", "Cluster P_{t} Selection with timing cut", cuts_pi0, 10., 3.));
		selections->Add(new AliPP13PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0));
		selections->Add(new AliPP13TagAndProbeSelection("TagAndProbleTOF", "Cluster P_{t} Selection", cuts_pi0));
		selections->Add(new AliPP13NonlinearityScanSelection("StudyNonlin", "Corrected for nonlinearity Physics Selection",cuts_pi0, nonlin_a, nonlin_b, ge_scale));
	}


	if (isMC)
	{
		selections->Add(new AliPP13PhysPhotonSelectionMC("PhysNonlin", "Corrected for nonlinearity Physics Selection",cuts_pi0, nonlin_a, nonlin_b, ge_scale));
		selections->Add(new AliPP13PhysPhotonSelectionMC("PhysRaw", "Raw Physics Selection", cuts_pi0));

		selections->Add(new AliPP13MesonSelectionMC("MCStudy", "MC Selection with timing cut", cuts_pi0,
			nonlin_a, nonlin_b, ge_scale, 
			weigh_a, weigh_b));

		selections->Add(new AliPP13QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0));
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
