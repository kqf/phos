void AddTasksTriggerQA(char * fname = "TriggerQA.root", char * contname = "PHOSTriggerQAResults")
{

    AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
    if (!mgr)
    {
        ::Error("AddTaskPHOSTriggerQA", "No analysis manager to connect to");
        return NULL;
    }

    if (!mgr->GetInputEventHandler())
    {
        ::Error("AddTaskPHOSTriggerQA", "This task requires an input event handler");
        return NULL;
    }
    
    TString labels[4] = {"L0", "L1medium", "L1high", "L1low"};
    for(int i = 0; i < 4; ++i)
    {
        AliAnalysisTaskPHOSTriggerQA * task = new AliAnalysisTaskPHOSTriggerQA("TriggerQA" + labels[i]);
        task->SelectL1Threshold(i - 1); // L0 == -1
        task->SelectCollisionCandidates(AliVEvent::kINT7);
        mgr->AddTask(task);
        mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());
        mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname + labels[i], TList::Class(), AliAnalysisManager::kOutputContainer, fname));
    }
}