TString  AddTaskCaloCellsQAPt(UInt_t offlineTriggerMask, std::vector<int> cells, const char * name = "CaloCellsQA2" )
{
    AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
    if (!mgr) return;

    AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
    if (!plugin) return;

    cout << "There are  " <<  cells.size()  << " excluded cells."<< endl;


    const Int_t nexc = cells.size();
    Int_t excel[nexc];

    // NB: Don't use copy. As it works bad with root
    // TODO: Move this function to the class method
    for(Int_t i = 0; i < cells.size(); ++i)
        excel[i] = cells[i];

    // Second Task
    AliAnalysisTaskCaloCellsQAPt * taskPHOSCellQA = TuneCaloCellsQAPt(5, 1, TString(name) + ".root", name);
    taskPHOSCellQA->GetCaloCellsQA()->SetClusterEnergyCuts(0.3, 0.3, 1.0);

    if (cells.size()) 
        taskPHOSCellQA->SetBadCells(excel, cells.size());
    taskPHOSCellQA->SetPairPtCut(1); // 2 GeV cut
    taskPHOSCellQA->SelectCollisionCandidates(offlineTriggerMask);

    TString sources = plugin->GetAnalysisSource();
    TString libs   = plugin->GetAdditionalLibs();
    
    plugin->SetAnalysisSource(sources + " AliAnalysisTaskCaloCellsQAPt.h ");
    plugin->SetAdditionalLibs(libs + " AliAnalysisTaskCaloCellsQAPt.h ");
    return  + TString(name) + ".root "; // Note extra space
}

AliAnalysisTaskCaloCellsQAPt * TuneCaloCellsQAPt(Int_t nmods = 10, Int_t det = 0, char * fname = "CellsQA.root", char * contname = NULL)
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