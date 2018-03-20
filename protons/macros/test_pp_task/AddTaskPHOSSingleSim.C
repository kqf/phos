AliAnalysisTaskPHOSSingleSim* AddTaskPHOSSingleSim(
    const char* name     = "SingleSim",
    const char* parname     = "Pi0"
    )
{
  //Add a task AliAnalysisTaskPHOSSingleSim to the analysis train
  //Author: Daiki Sekihata
  /* $Id$ */

  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr) {
    ::Error("AddTaskPHOSPi0EtaToGammaGamma", "No analysis manager to connect to");
    return NULL;
  }
  
  if (!mgr->GetInputEventHandler()) {
    ::Error("AddTaskPHOSPi0EtaToGammaGamma", "This task requires an input event handler");
    return NULL;
  }


  TString taskname = Form("%s_%s",name,parname);

  AliAnalysisTaskPHOSSingleSim* task = new AliAnalysisTaskPHOSSingleSim(taskname);
  //task->SelectCollisionCandidates(trigger);//no trigger selection in single simulation

  mgr->AddTask(task);
  mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer() );
 
  TString outputFile = AliAnalysisManager::GetCommonFileName();
  TString prefix = Form("hist_%s",taskname.Data());

  AliAnalysisDataContainer *coutput1 = mgr->CreateContainer(Form("%s",prefix.Data()), THashList::Class(), AliAnalysisManager::kOutputContainer, Form("%s:%s",outputFile.Data(),"PWGGA_PHOSTasks_PHOSRun2"));
  mgr->ConnectOutput(task, 1, coutput1);

  return task;
}

