TString AddAnalysisTaskPP(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "", Int_t * excells = 0, Int_t nexc = 0)
{

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

    gROOT->LoadMacro("PhotonSelection.cxx+");
    gROOT->LoadMacro("GeneralPhotonSelection.cxx+");
    gROOT->LoadMacro("PhotonSpectrumSelection.cxx+");
    gROOT->LoadMacro("QualityPhotonSelection.cxx+");
    gROOT->LoadMacro("TestPhotonSelection.cxx+");
    gROOT->LoadMacro("PhotonTimecutSelection.cxx+");
    gROOT->LoadMacro("PhysPhotonSelection.cxx+");
    gROOT->LoadMacro("MixingSample.h+");
    gROOT->LoadMacro("AliAnalysisTaskPP.cxx+");
  
	// Setup Selections
	TList * selections = new TList();

	selections->Add(new PhysPhotonSelection("Phys", "Physics Selection", 0.3, 1.0, 3, 12.5e-9));
	selections->Add(new PhotonTimecutSelection("Time", "Testing Timing Selection", 0.3, 1.0, 3, 12.5e-9));

	selections->Add(new PhysPhotonSelection("Eta", "Physics Selection for eta meson", 0.3, 0.7, 3, 12.5e-9));
	selections->Add(new PhotonTimecutSelection("EtaTime", "Testing Timing Selection for eta meson", 0.3, 0.7, 3, 12.5e-9));
	
	GeneralPhotonSelection * sel = new QualityPhotonSelection("Qual", "Cluster quality Selection");
	sel->SetTimingCut(12.5e-9);
	selections->Add(sel);

	selections->Add(new PhotonSpectrumSelection("Photons", "Cluster P_{t} Selection"));
	selections->Add(new PhotonSpectrumSelection("PhotonsTime", "Cluster P_{t} Selection with timing cut", 0.3, 1.0, 3, 12.5e-9, 10., 3.));
	

	// Setup task
	AliAnalysisTaskPP * task = new AliAnalysisTaskPP("PhosProtons", selections);

	if ( !badmap.IsNull() ) 
		task->SetBadMap(badmap);

	if ( nexc > 0 ) 
		task->SetBadCells(excells, nexc);

	if ( (nexc > 0) && (!badmap.IsNull())) 
		cout << "Warning, you are setting bad cells and bad map! Be sure that you know what you are doing" << endl;

	// task->GetSelections()->Add
	task->SelectCollisionCandidates(offlineTriggerMask);
	mgr->AddTask(task);



	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	AliAnalysisDataContainer * coutput = 0;
	for (int i = 0; i < task->GetSelections()->GetEntries(); ++ i)
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
	    "PhotonSelection.cxx " +
	    "GeneralPhotonSelection.cxx " +
	    "PhotonSpectrumSelection.cxx " +
	    "QualityPhotonSelection.cxx " +
	    "TestPhotonSelection.cxx " +
	    "PhysPhotonSelection.cxx " +
	    "PhotonTimecutSelection.cxx " +
	    "MixingSample.h " +
	    "AliAnalysisTaskPP.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
	    "PhotonSelection.cxx " +
	    "PhotonSelection.h " +
	    "GeneralPhotonSelection.cxx " +
	    "GeneralPhotonSelection.h " +
	    "PhotonSpectrumSelection.cxx " +
	    "PhotonSpectrumSelection.h " +
	    "QualityPhotonSelection.cxx " +
	    "QualityPhotonSelection.h " +
	    "TestPhotonSelection.cxx " +
	    "TestPhotonSelection.h " +
	    "PhysPhotonSelection.cxx " +
	    "PhysPhotonSelection.h " +
	    "PhotonTimecutSelection.cxx " +
	    "PhotonTimecutSelection.h " +
	    "MixingSample.h " +
	    "AliAnalysisTaskPP.cxx " +
	    "AliAnalysisTaskPP.h " 
	);

	return TString(AliAnalysisManager::GetCommonFileName()) + " ";  // This extra space is important
}
