AliAnalysisTaskCaloCellsQA* AddTaskCaloCellsPhysQA(Int_t nmods = 10, Int_t det = 0,
                                               TString fname = "CellsQA.root", TString contname = "")
{
  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr) {
    ::Error("AddTaskCaloCellsPhysQA", "No analysis manager to connect to");
    return NULL;
  }

  // check the analysis type using the event handlers connected to the analysis manager
  if (!mgr->GetInputEventHandler()) {
    ::Error("AddTaskCaloCellsPhysQA", "This task requires an input event handler");
    return NULL;
  }

  // Configure analysis
  //===========================================================================

  // detector number
  Int_t det2 = -1;
  if       (det == 0) det2 = AliAnalysisTaskCaloCellsQA::kEMCAL;
  else  if (det == 1) det2 = AliAnalysisTaskCaloCellsQA::kPHOS;
  else
  ::Fatal("AddTaskCaloCellsPhysQA", "Wrong detector provided");

  AliAnalysisTaskCaloCellsQA* task;

  if ((fname.Length() != 0) && (contname.Length() == 0)) task = new AliAnalysisTaskCaloCellsPhysQA("AliAnalysisTaskCaloCellsQA", nmods, det2, fname.Data());
  else                    task = new AliAnalysisTaskCaloCellsPhysQA("AliAnalysisTaskCaloCellsQA", nmods, det2);
  mgr->AddTask(task);

  mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer());

  // container output into particular file
  if ((fname.Length() != 0) && (contname.Length() != 0))
    mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(),
                             TObjArray::Class(), AliAnalysisManager::kOutputContainer, fname.Data()));

  // container output into common file
  if ((fname.Length() == 0)) {
    if (contname.Length() == 0) contname = "CellsQAResults";
      mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(),
                               TObjArray::Class(), AliAnalysisManager::kOutputContainer, mgr->GetCommonFileName()));
  }
  return task;
}
