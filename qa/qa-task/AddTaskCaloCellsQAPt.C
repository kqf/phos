AliAnalysisTaskCaloCellsQAPt * AddTaskCaloCellsQAPt(Int_t nmods = 10, Int_t det = 0,
        char * fname = "CellsQA.root", char * contname = NULL)
{
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
	{
		::Error("AddTaskCaloCellsQA", "No analysis manager to connect to");
		return NULL;
	}

	// check the analysis type using the event handlers connected to the analysis manager
	if (!mgr->GetInputEventHandler())
	{
		::Error("AddTaskCaloCellsQA", "This task requires an input event handler");
		return NULL;
	}

	// Configure analysis
	//===========================================================================

	// detector number
	Int_t det2 = -1;
	if (det == 1) det2 = AliAnalysisTaskCaloCellsQAPt::kPHOS;
	else
		::Fatal("AddTaskCaloCellsQA", "Wrong detector provided");

	AliAnalysisTaskCaloCellsQAPt * task;

	if (fname && !contname) task = new AliAnalysisTaskCaloCellsQAPt("AliAnalysisTaskCaloCellsQAPt", nmods, det2, fname);
	else                    task = new AliAnalysisTaskCaloCellsQAPt("AliAnalysisTaskCaloCellsQAPt", nmods, det2);
	mgr->AddTask(task);

	mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());

	// container output into particular file
	if (fname && contname)
		mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname,
		                   TObjArray::Class(), AliAnalysisManager::kOutputContainer, fname));

	// container output into common file
	if (!fname)
	{
		if (!contname) contname = "CellsQAResults";
		mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname,
		                   TObjArray::Class(), AliAnalysisManager::kOutputContainer, mgr->GetCommonFileName()));
	}

	return task;
}