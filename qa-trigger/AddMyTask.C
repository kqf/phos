AliAnalysisTaskSE * AddMyTask()
{
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
    // Second Task

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

	AliAnalysisTaskSE * task = new AliAnalysisTaskPHOSTriggerQAPerRun("PhosTriggerTest");
	task->SelectCollisionCandidates(AliVEvent::kINT7);
	mgr->AddTask(task);

	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	coutput = mgr->CreateContainer("Data",
	                               TList::Class(),
	                               AliAnalysisManager::kOutputContainer,
	                               AliAnalysisManager::GetCommonFileName());
	mgr->ConnectOutput(task, 1, coutput);
	return task;
}
