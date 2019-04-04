#include "AliAnalysisTaskPHOSTriggerQAv1.cxx+"

void LoadAnalysisLibraries()
{
  AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr)
  {
    cerr << "Fatal: There is no analysis manager" << endl;
    return;
  }
  AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
  TString sources = plugin->GetAnalysisSource();
  TString libs   = plugin->GetAdditionalLibs();
  plugin->SetAnalysisSource(
    sources +
    "AliAnalysisTaskPHOSTriggerQAv1.cxx "
  );

  plugin->SetAdditionalLibs(
    libs +
    "libPWGGAPHOSTasks.so " +
    "AliAnalysisTaskPHOSTriggerQAv1.cxx " +
    "AliAnalysisTaskPHOSTriggerQAv1.h "
  );
}

AliAnalysisTaskPHOSTriggerQAv1* AddTaskPHOSTriggerQAv1(TString fname = "PHOSTriggerQA.root", TString contname = "")
{
  //Add PHOS trigger QA task to the PWGPP QA train.

  LoadAnalysisLibraries();
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
    mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(), TList::Class(), AliAnalysisManager::kOutputContainer, fname.Data()));

  // container output into common file
  if (fname.Length() == 0) {
    if (contname.Length() == 0) contname = "PHOSTriggerQAResults";
    mgr->ConnectOutput(task, 1, mgr->CreateContainer(contname.Data(), TList::Class(), AliAnalysisManager::kOutputContainer, mgr->GetCommonFileName()));
  }

  return task;
}
