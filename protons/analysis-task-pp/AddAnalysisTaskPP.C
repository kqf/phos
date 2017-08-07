TString AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "", const std::vector<Int_t>  & v, Bool_t isMC = kFALSE, Bool_t isTest = kFALSE)
{
	cout << "Setting cells " <<  v.size() << endl;
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

    gROOT->LoadMacro("ClusterCuts.cxx+");
    gROOT->LoadMacro("DetectorHistogram.cxx+");
    gROOT->LoadMacro("PhotonSelection.cxx+");
    gROOT->LoadMacro("PhotonSpectrumSelection.cxx+");
    gROOT->LoadMacro("QualityPhotonSelection.cxx+");
    gROOT->LoadMacro("ParticlesHistogram.cxx+");
    gROOT->LoadMacro("PhotonTimecutStudySelection.cxx+");
    gROOT->LoadMacro("PhysPhotonSelection.cxx+");
    gROOT->LoadMacro("TagAndProbeSelection.cxx+");
    gROOT->LoadMacro("MesonSelectionMC.cxx+");
    gROOT->LoadMacro("PythiaInfoSelection.cxx+");
    gROOT->LoadMacro("PhysPhotonSelectionMC.cxx+");
    gROOT->LoadMacro("NonlinearityScanSelection.cxx+");
    gROOT->LoadMacro("MixingSample.cxx+");
    gROOT->LoadMacro("AliAnalysisTaskPP.cxx+");

    // exit(1);
  
	// Setup Selections
	TList * selections = new TList();

	ClusterCuts cuts_pi0 = ClusterCuts::GetClusterCuts();
	ClusterCuts cuts_eta = ClusterCuts::GetClusterCuts();
	cuts_eta.fAsymmetryCut = 0.7;

	if (!isTest && !isMC)
	{
		selections->Add(new PhysPhotonSelection("Phys", "Physics Selection", cuts_pi0));
		selections->Add(new PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0));

		selections->Add(new PhysPhotonSelection("Eta", "Physics Selection for eta meson", cuts_eta));
		selections->Add(new PhotonTimecutStudySelection("EtaTime", "Testing Timing Selection for eta meson", cuts_eta));
		
		selections->Add(new QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0));
		selections->Add(new PhotonSpectrumSelection("Photons", "Cluster P_{t} Selection", cuts_pi0));
		selections->Add(new PhotonSpectrumSelection("PhotonsTime", "Cluster P_{t} Selection with timing cut", cuts_pi0, 10., 3.));
	}	

	
	if(isTest)
	{
		selections->Add(new PhysPhotonSelection("Phys", "Physics Selection", cuts_pi0));
	}


	if (isMC)
	{
		// Float_t nonlin_a = -1.84679e-02;
		// Float_t nonlin_b = -4.70911e-01;
		// Float_t nonlin_a = 0;
		// Float_t nonlin_b = 1;

		// Nonlinearity for zs 25 LHC16all
		//
		
		// Float_t nonlin_a = -6.90763e-03;
		// Float_t nonlin_b = -1.74981e+00;


		// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
		// The pi^0 peak is misplaced in this fit: A * 1.03274e+00 (global energy scale)
		// 
		// 

	    Float_t ge_scale = 1.04408e+00;
		Float_t nonlin_a = -2.00071e-02;
		Float_t nonlin_b = 1.24818e+00;

		// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
		// Now using Daiki's parameters, and no extra x/2, x/2 factors
		// Global energy scale: A * 1.04
		// 
		// Float_t nonlin_a = -0.05;
		// Float_t nonlin_b = 0.6;
	    // Float_t ge_scale = 1.04;

		selections->Add(new PhysPhotonSelectionMC("PhysNonlin", "Corrected for nonlinearity Physics Selection",cuts_pi0, nonlin_a, nonlin_b, ge_scale));
		selections->Add(new PhysPhotonSelectionMC("PhysRaw", "Raw Physics Selection", cuts_pi0));
		selections->Add(new MesonSelectionMC("MCStudy", "MC Selection with timing cut", cuts_pi0));
		selections->Add(new QualityPhotonSelection("Qual", "Cluster quality Selection", cuts_pi0));

		if(suff.Contains("Only") && IsJetJetMC(description, isMC))
			selections->Add(new PythiaInfoSelection("PythiaInfo", "Cross section and ntrials for a pthard bin."));


		// Test selections
		selections->Add(new TagAndProbeSelection("TagAndProble", "Cluster P_{t} Selection", cuts_pi0));
		selections->Add(new PhotonSpectrumSelection("PhotonsTime", "Cluster P_{t} Selection with timing cut", cuts_pi0, 10., 3.));
		selections->Add(new PhotonTimecutStudySelection("Time", "Testing Timing Selection", cuts_pi0));
		selections->Add(new NonlinearityScanSelection("StudyNonlin", "Corrected for nonlinearity Physics Selection",cuts_pi0, nonlin_a, nonlin_b, ge_scale));
	}

	// Setup task
	AliAnalysisTaskPP * task = new AliAnalysisTaskPP("PhosProtons", selections);

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
		PhotonSelection * fSel = dynamic_cast<PhotonSelection *> (task->GetSelections()->At(i));
		fSel->SetTitle(description);
		cout << fSel->GetTitle() << endl;

		coutput = mgr->CreateContainer(fSel->GetName() + suff,
		                               TList::Class(),
		                               AliAnalysisManager::kOutputContainer,
		                               AliAnalysisManager::GetCommonFileName());
		mgr->ConnectOutput(task, i + 1, coutput);
	}

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
	    "ClusterCuts.cxx " +
	    "DetectorHistogram.cxx " +
	    "PhotonSelection.cxx " +
	    "PhotonSpectrumSelection.cxx " +
	    "QualityPhotonSelection.cxx " +
	    "ParticlesHistogram.cxx " +
	    "PhysPhotonSelection.cxx " +
	    "PhotonTimecutStudySelection.cxx " +
	    "TagAndProbeSelection.cxx " +
	    "MesonSelectionMC.cxx " +
	    "PythiaInfoSelection.cxx " +
	    "PhysPhotonSelectionMC.cxx " +
	    // "NonlinearityScanSelection.cxx " +
	    "MixingSample.cxx " +
	    "AliAnalysisTaskPP.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
	    "ClusterCuts.cxx " +
	    "ClusterCuts.h " +
	    "DetectorHistogram.cxx " +
	    "DetectorHistogram.h " +
	    "PhotonSelection.cxx " +
	    "PhotonSelection.h " +
	    "PhotonSpectrumSelection.cxx " +
	    "PhotonSpectrumSelection.h " +
	    "QualityPhotonSelection.cxx " +
	    "QualityPhotonSelection.h " +
	    "ParticlesHistogram.cxx " +
	    "ParticlesHistogram.h " +
	    "PhysPhotonSelection.cxx " +
	    "PhysPhotonSelection.h " +
	    "PhotonTimecutStudySelection.cxx " +
	    "PhotonTimecutStudySelection.h " +
	    "TagAndProbeSelection.cxx " +
	    "TagAndProbeSelection.h " +
	    "MesonSelectionMC.cxx " +
	    "MesonSelectionMC.h " +
	    "PhysPhotonSelectionMC.cxx " +
	    "PhysPhotonSelectionMC.h " +
	    "PythiaInfoSelection.cxx " +
	    "PythiaInfoSelection.h " +
	    "NonlinearityScanSelection.cxx " +
	    "NonlinearityScanSelection.h " +
	    "MixingSample.cxx " +
	    "MixingSample.h " +
	    "AliAnalysisTaskPP.cxx " +
	    "AliAnalysisTaskPP.h " 
	);

	return TString(AliAnalysisManager::GetCommonFileName()) + " ";  // This extra space is important
}

Bool_t IsJetJetMC(TString description, Bool_t isMC)
{
	if(!isMC)
		return kFALSE;

	if(description.Contains("Jet-Jet"))
		return kTRUE;


	cout << "Not Using PythiaInfo!!! " << endl;

	// Don't include Jet-Jet counters by default
	return kFALSE;
}
