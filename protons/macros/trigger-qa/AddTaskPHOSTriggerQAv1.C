AliAnalysisTaskPHOSTriggerQAv1* AddTaskPHOSTriggerQAv1(TString fname="PHOSTriggerQA.root", TString contname="")
{
  //Add PHOS trigger QA task to the PWGPP QA train.

  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr) {
    ::Error("AddTaskPHOSTriggerQAv1", "No analysis manager to connect to");
    return NULL;
  }
  
  if (!mgr->GetInputEventHandler()) {
    ::Error("AddTaskPHOSTriggerQAv1", "This task requires an input event handler");
    return NULL;
  }

  AliAnalysisTaskPHOSTriggerQAv1* task = new AliAnalysisTaskPHOSTriggerQAv1("PHOSTriggerQA");
  mgr->AddTask(task);

  mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());

  // container output into particular file
  if (fname.Length() != 0 && contname.Length() != 0)
    mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(),TList::Class(), AliAnalysisManager::kOutputContainer, fname.Data()));
  
  // container output into common file
  if (fname.Length() == 0) {
    if (contname.Length() == 0) contname = "PHOSTriggerQAResults";
    mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(),TList::Class(), AliAnalysisManager::kOutputContainer, mgr->GetCommonFileName()));      
  }
  
  return task;
}