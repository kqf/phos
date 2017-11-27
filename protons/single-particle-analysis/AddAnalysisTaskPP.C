void AddAnalysisTaskPP(TString description, TString suff = "", TString badmap = "", const std::vector<Int_t>  & v)
{
	cout << "Setting cells " <<  v.size() << endl;
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) 
	{
		cerr << "Fatal: There is no analysis manager" << endl;
		return;
	}

    gROOT->LoadMacro("AliPP13ClusterCuts.cxx+");
    gROOT->LoadMacro("AliPP13SelectionWeights.cxx+");
    gROOT->LoadMacro("AliPP13DetectorHistogram.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSpectrumSelection.cxx+");
    gROOT->LoadMacro("AliPP13QualityPhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13ParticlesHistogram.cxx+");
    gROOT->LoadMacro("AliPP13PhotonTimecutStudySelection.cxx+");
    gROOT->LoadMacro("AliPP13PhysPhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13TagAndProbeSelection.cxx+");
    gROOT->LoadMacro("AliPP13PythiaInfoSelection.cxx+");
    gROOT->LoadMacro("AliPP13PhysPhotonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13NonlinearitySelection.cxx+");
    gROOT->LoadMacro("AliPP13EfficiencySelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13MesonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13NonlinearityScanSelection.cxx+");
    gROOT->LoadMacro("AliPP13MixingSample.cxx+");
    gROOT->LoadMacro("AliAnalysisTaskPP13.cxx+");

    // exit(1);
  
	// Setup Selections
	TList * selections = new TList();

	AliPP13ClusterCuts cuts_pi0 = AliPP13ClusterCuts::GetClusterCuts();
	AliPP13ClusterCuts cuts_eta = AliPP13ClusterCuts::GetClusterCuts();


    // exit(1);

	// This will fix the problem with Single particle MC
	
	cuts_pi0.fNContributors = 0;
	cuts_eta.fNContributors = 0;
	cuts_eta.fAsymmetryCut = 0.7;

	// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
	// The pi^0 peak is misplaced in this fit: A * 1.03274e+00 (global energy scale)
	// Calculated for the updated version for the corrected Data
	
	// Float_t nonlin_a = -0.020025549129372242;
	// Float_t nonlin_b = 1.1154536660217529;
	// Float_t ge_scale = 1.0493128193171741;

	// Nonlinearity for zs 20 Run2Default (Daiki's approximation)
	// Calculated on single particle MC
	//
	
	Float_t nonlin_a = -0.024603176300721907;
	Float_t nonlin_b =  1.1443886239082113;
    Float_t ge_scale =  1.0560164522642017;


	// Float_t weigh_a = -1.063;
	// Float_t weigh_b = 0.855;

	// Float_t nonlin_a = 0;
	// Float_t nonlin_b = 1.;
    // Float_t ge_scale = 1.;

    Float_t weigh_a = 0;
    Float_t weigh_b = 1.;


	selections->Add(new AliPP13PhysPhotonSelectionMC("PhysRaw", "Raw Physics Selection", cuts_pi0));
	selections->Add(new AliPP13PhysPhotonSelectionMC("PhysNonlin", "Corrected for nonlinearity Physics Selection",cuts_pi0, nonlin_a, nonlin_b, ge_scale));
	
	AliPP13SelectionWeights spmc_weights = AliPP13SelectionWeights::Init(AliPP13SelectionWeights::kSinglePi0MC);
	selections->Add(new AliPP13NonlinearitySelection("PhysNonlinEst", "Physics efficiency for neutral particles", cuts_pi0, spmc_weights));
	selections->Add(new AliPP13EfficiencySelectionMC("PhysEff", "Physics efficiency for neutral particles", cuts_pi0, spmc_weights));

	selections->Add(new AliPP13MesonSelectionMC("MCStudy", "MC Selection with timing cut", cuts_pi0,
		nonlin_a, nonlin_b, ge_scale, 
		weigh_a, weigh_b));

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

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
	    "AliPP13ClusterCuts.cxx " +
	    "AliPP13SelectionWeights.cxx " +
	    "AliPP13DetectorHistogram.cxx " +
	    "AliPP13PhotonSelection.cxx " +
	    "AliPP13PhotonSelectionMC.cxx " +
	    "AliPP13PhotonSpectrumSelection.cxx " +
	    "AliPP13QualityPhotonSelection.cxx " +
	    "AliPP13ParticlesHistogram.cxx " +
	    "AliPP13PhysPhotonSelection.cxx " +
	    "AliPP13PhotonTimecutStudySelection.cxx " +
	    "AliPP13TagAndProbeSelection.cxx " +
	    "AliPP13PythiaInfoSelection.cxx " +
	    "AliPP13PhysPhotonSelectionMC.cxx " +
	    "AliPP13MesonSelectionMC.cxx " +
	    "AliPP13NonlinearitySelection.cxx " +
	    "AliPP13EfficiencySelectionMC.cxx " +
	    "AliPP13NonlinearityScanSelection.cxx " +
	    "AliPP13MixingSample.cxx " +
	    "AliAnalysisTaskPP13.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
	    "AliPP13ClusterCuts.cxx " +
	    "AliPP13ClusterCuts.h " +
	    "AliPP13SelectionWeights.cxx " +
	    "AliPP13SelectionWeights.h " +
	    "AliPP13DetectorHistogram.cxx " +
	    "AliPP13DetectorHistogram.h " +
	    "AliPP13PhotonSelection.cxx " +
	    "AliPP13PhotonSelection.h " +
	    "AliPP13PhotonSelectionMC.cxx " +
	    "AliPP13PhotonSelectionMC.h " +
	    "AliPP13PhotonSpectrumSelection.cxx " +
	    "AliPP13PhotonSpectrumSelection.h " +
	    "AliPP13QualityPhotonSelection.cxx " +
	    "AliPP13QualityPhotonSelection.h " +
	    "AliPP13ParticlesHistogram.cxx " +
	    "AliPP13ParticlesHistogram.h " +
	    "AliPP13PhysPhotonSelection.cxx " +
	    "AliPP13PhysPhotonSelection.h " +
	    "AliPP13PhotonTimecutStudySelection.cxx " +
	    "AliPP13PhotonTimecutStudySelection.h " +
	    "AliPP13TagAndProbeSelection.cxx " +
	    "AliPP13TagAndProbeSelection.h " +
	    "AliPP13PhysPhotonSelectionMC.cxx " +
	    "AliPP13PhysPhotonSelectionMC.h " +
	    "AliPP13PythiaInfoSelection.cxx " +
	    "AliPP13PythiaInfoSelection.h " +
	    "AliPP13NonlinearitySelection.h " +
	    "AliPP13NonlinearitySelection.cxx " +
	    "AliPP13EfficiencySelectionMC.cxx " +
	    "AliPP13EfficiencySelectionMC.h " +
	    "AliPP13MesonSelectionMC.cxx " +
	    "AliPP13MesonSelectionMC.h " +
	    "AliPP13NonlinearityScanSelection.cxx " +
	    "AliPP13NonlinearityScanSelection.h " +
	    "AliPP13MixingSample.cxx " +
	    "AliPP13MixingSample.h " +
	    "AliAnalysisTaskPP13.cxx " +
	    "AliAnalysisTaskPP13.h " 
	);
}
