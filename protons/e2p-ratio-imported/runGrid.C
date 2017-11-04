{
  // Load common libraries
  gSystem->Load("libCore");  
  gSystem->Load("libTree");
  gSystem->Load("libGeom");
  gSystem->Load("libVMC");
  gSystem->Load("libPhysics");
  gSystem->Load("libMinuit");
  gSystem->Load("libGui");
  gSystem->Load("libXMLParser");
  gSystem->Load("libMinuit2");

  gSystem->Load("libProof");
  gSystem->Load("libSTEERBase");
  gSystem->Load("libESD");
  gSystem->Load("libAOD");
  gSystem->Load("libOADB");
  gSystem->Load("libANALYSIS");
  gSystem->Load("libANALYSISalice");
  gSystem->Load("libCDB");
  gSystem->Load("libRAWDatabase");
  gSystem->Load("libSTEER");
  gSystem->Load("libCORRFW");

  gSystem->Load("libPHOSUtils");
  gSystem->Load("libPHOSbase");
  gSystem->Load("libPHOSsim"); 
  gSystem->Load("libPHOSrec");
  gSystem->Load("libPHOSshuttle"); 
  gSystem->Load("libTender");
  gSystem->Load("libTenderSupplies");
  gSystem->Load("libANALYSISalice.so");
  gSystem->Load("libPWGCaloTrackCorrBase");
  gSystem->Load("libPWGGACaloTrackCorrelations");
  gSystem->Load("libPWGGAPHOSTasks");
  gSystem->Load("libPHOSpi0Calib");
  gSystem->Load("libPWGGAUtils"); 

  gROOT->ProcessLine(".include $ALICE_ROOT/include");
  gSystem->AddIncludePath ("-I. -I$ROOTSYS/include -I$ALICE_ROOT -I$ALICE_ROOT/include -I$ALICE_PHYSICS -I$ALICE_PHYSICS/include -I$ALICE_ROOT/ITS -I$ALICE_ROOT/TPC -I$ALICE_ROOT/CONTAINERS -I$ALICE_ROOT/STEER/STEER -I$ALICE_ROOT/STEER/STEERBase -I$ALICE_ROOT/STEER/ESD -I$ALICE_ROOT/STEER/AOD -I$ALICE_ROOT/TRD -I$ALICE_PHYSICS/macros -I$ALICE_PHYSICS/ANALYSIS  -I$ALICE_PHYSICS/OADB -I$ALICE_PHYSICS/PHOS -I$ALICE_PHYSICS/PWGGA -g");
  
 
  AliAnalysisManager *mgr = new AliAnalysisManager("MyTask");
  gROOT->LoadMacro("CreateAlienHandler.C");
  AliAnalysisGrid *alienHandler = CreateAlienHandler();  
  if (!alienHandler) return;
  mgr->SetGridHandler(alienHandler);

  AliAODInputHandler* aodH = new AliAODInputHandler();
  mgr->SetInputEventHandler(aodH);
   
  //Tender supply
  gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
  AliPHOSTenderTask *tender = AddAODPHOSTender("PHOSTenderTask","PHOStender","",4,kFALSE);
  AliPHOSTenderSupply *supply = tender->GetPHOSTenderSupply();
  supply->ForceUsingBadMap("BadMap_LHC10ef_Majority300416.root");

  gROOT->LoadMacro("$ALICE_ROOT/ANALYSIS/macros/AddTaskPIDResponse.C");
  cout<<"I am adding PID response task"<<endl;
  /* AliAnalysisTask *AddTaskPIDResponse(Bool_t isMC=kFALSE, Bool_t autoMCesd=kTRUE,
                                    Bool_t tuneOnData=kFALSE, Int_t recoPass=2,
                                    Bool_t cachePID=kFALSE, TString detResponse="",
                                    Bool_t useTPCEtaCorrection = kTRUE,
                                    Bool_t useTPCMultiplicityCorrection = kFALSE,
				    Int_t  recoDataPass = -1)*/
  AliAnalysisTaskPIDResponse *taskPID=AddTaskPIDResponse(kFALSE,kTRUE,kTRUE,4,kFALSE,"",kTRUE,kFALSE,4);
  
  gROOT->LoadMacro("AliAnalysisTaskEpRatiopp.cxx++g");
  gROOT->LoadMacro("AddTaskPHOSEpRatiopp.C");

  //Add e/p Tasks
  AliAnalysisTaskEpRatiopp *mytask = AddTaskPHOSEpRatiopp(kFALSE,"PHOSEpRatio","", AliVEvent::kMB);
  // mgr->AddTask(mytask);
  
  mgr->SetDebugLevel(0);
  if (!mgr->InitAnalysis()) return;
  mgr->PrintStatus();
  mgr->StartAnalysis("grid");
};
