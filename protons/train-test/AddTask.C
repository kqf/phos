AliAnalysisTaskExample *AddTask(Double_t variable, const char* suffix = "")
{
  // Get the pointer to the existing analysis manager via the static access method.
  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr) {    ::Error("AddTask", "No analysis manager to connect to.");
    return NULL;
  }  
  
  // Create the task and configure it.
  TString combinedName;
  combinedName.Form("MyTask%s", suffix);
  AliAnalysisTaskExample* ana = new AliAnalysisTaskExample(combinedName);

  //set a custom variable for your task
  ana->SetVariable(variable);
  
  //add the task to the analysis manager
  mgr->AddTask(ana);
  
  // Create ONLY the output containers for the data produced by the task.
  // Get and connect other common input/output containers via the manager as below
  char* outputFileName = AliAnalysisManager::GetCommonFileName();
  
  AliAnalysisDataContainer *coutput = mgr->CreateContainer(combinedName, TList::Class(), AliAnalysisManager::kOutputContainer, Form("%s:%s", outputFileName, "PWGZZ_MyFolder"));
  
  mgr->ConnectInput  (ana, 0, mgr->GetCommonInputContainer());
  mgr->ConnectOutput (ana, 1, coutput ); //connect your task to the output container
   
  return ana;
}
