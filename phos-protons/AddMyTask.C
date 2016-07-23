AliAnalysisTaskPrompt * AddMyTask(UInt_t offlineTriggerMask, TString description, TString suff = "", TString badmap = "",Int_t * excells = 0, Int_t nexc = 0)
{
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

	AliAnalysisTaskPrompt * task = new AliAnalysisTaskPrompt("PhosProtons");
	if( !badmap.IsNull() ) task->SetBadMap(badmap);
    if(nexc > 0) task->SetBadCells(excells, nexc);
    if( (nexc > 0) && (!badmap.IsNull())) cout << "Warning, you are setting bad cells and bad map! Be sure that you know what you are doing" << endl;

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

	return task;
}
