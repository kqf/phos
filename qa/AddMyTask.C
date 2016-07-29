AliAnalysisTaskSE * AddMyTask(Int_t * excells, Int_t nexc)
{
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

	for(int i = 0; i < nexc; ++i)
		cout << " " << excells[i] << endl;

	cout << " there are nexc " <<  nexc	 << endl;

	if(!excells) cout << "ERRROR\nERRROR\nERRROR\nERRROR\nCells are not set" << endl;

	gROOT->LoadMacro("AddTaskCaloCellsQAPt.C");

	AliAnalysisTaskCaloCellsQAPt * taskPHOSCellQA = AddTaskCaloCellsQAPt(5, 1, "CaloCellsQA1.root", "PHOSCellsQA1");
	taskPHOSCellQA->GetCaloCellsQA()->SetClusterEnergyCuts(0.3, 0.3, 1.0);

	if(excells) taskPHOSCellQA->SetBadCells(excells, nexc);
    taskPHOSCellQA->SetPairPtCut(1); // 1 GeV cut
    taskPHOSCellQA->SelectCollisionCandidates(AliVEvent::kINT7);

    // Second Task
    taskPHOSCellQA = AddTaskCaloCellsQAPt(5, 1, "CaloCellsQA2.root", "PHOSCellsQA2");
    taskPHOSCellQA->GetCaloCellsQA()->SetClusterEnergyCuts(0.3, 0.3, 1.0);

    if(excells) taskPHOSCellQA->SetBadCells(excells, nexc);
    taskPHOSCellQA->SetPairPtCut(2); // 2 GeV cut
    taskPHOSCellQA->SelectCollisionCandidates(AliVEvent::kINT7);
	return taskPHOSCellQA;
}
