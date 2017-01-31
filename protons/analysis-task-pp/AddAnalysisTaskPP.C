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

	selections->Add(new PhysPhotonSelection("Phys", "Physics Selection"));
	selections->Add(new PhotonTimecutSelection("Time", "Timing Selection"));

	selections->Add(new PhysPhotonSelection("Eta", "Physics Selection for eta meson", 0.3, 0.7));
	selections->Add(new PhotonTimecutSelection("EtaTime", "Timing Selection for eta meson", 0.3, 0.7));
	
	selections->Add(new QualityPhotonSelection("Qual", "Cluster quality Selection"));
	
	selections->Add(new PhotonSpectrumSelection("Photons", "Cluster P_{t} Selection"));
	

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

	return TString(AliAnalysisManager::GetCommonFileName()) + " ";  // This extra space is important
}
