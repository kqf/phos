AliAnalysisTaskEpRatiopp* AddTaskPHOSEpRatiopp (Bool_t kMC = kFALSE,
					    const char* name = "PHOSEpRatio",
					    const char* options = "",
					    UInt_t offlineTriggerMask = AliVEvent::kINT7 )
{
  //Add a task AliAnalysisTaskEpRatiopp to the analysis train.
  //Author: Boris Polishchuk.
  
  AliAnalysisManager *mgr = AliAnalysisManager::GetAnalysisManager();
  if (!mgr) {
    ::Error("AddTaskPHOSEpRatiopp", "No analysis manager to connect to");
    return NULL;
  }
  
  if (!mgr->GetInputEventHandler()) {
    ::Error("AddTaskPHOSEpRatiopp", "This task requires an input event handler");
    return NULL;
  }
  

  AliAnalysisTaskEpRatiopp* task = new AliAnalysisTaskEpRatiopp(Form("%sTask", name));  
  
  /* TFile *fBadMap = TFile::Open("BadMap_LHC10ef_Majority300416.root");
     if(fBadMap->IsOpen()){
     printf("\n\n...Adding PHOS bad channel map \n") ;
     gROOT->cd();
     char key1[55] ;
     for(Int_t mod=1;mod<4; mod++){
     sprintf(key1,"PHOS_BadMap_mod%d",mod) ;
     TH2I * h = (TH2I*)fBadMap->Get(key1) ;
     if(h)
     task->SetPHOSBadMap(mod,h) ;
     }
     fBadMap->Close() ;
     }*/

  if(!kMC) task->SelectCollisionCandidates(offlineTriggerMask);
  mgr->AddTask(task);
  mgr->ConnectInput(task, 0, mgr->GetCommonInputContainer() );
  
  TString cname(Form("%sCoutput1", name));
  TString pname(Form("%s:%s", AliAnalysisManager::GetCommonFileName(), name));
  AliAnalysisDataContainer *coutput1 = mgr->CreateContainer(cname.Data(), TList::Class(), AliAnalysisManager::kOutputContainer, pname.Data());
  mgr->ConnectOutput(task, 1, coutput1);
  
  return task;
}
