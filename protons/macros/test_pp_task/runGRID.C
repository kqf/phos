//____________________________________________________________________________________________________________________________________
const TString kInputData   = "AOD"; //ESD, AOD
const TString kCollision   = "PbPb";
const TString period       = "LHC15o";
const Bool_t usePHOSTender = kTRUE;
const Bool_t usePAR        = kFALSE;
const TString pass         = "pass1";
const TString MCname       = "LHC17i7b2";
const TString MCtype       = "MBMC";
const Bool_t kMC           = kTRUE; //With real data kMC = kFALSE
const Bool_t kEmb          = kFALSE;
Bool_t kJJMC               = kFALSE;
const Bool_t FlowTask      = kFALSE;
const Bool_t NonLinCorr    = kTRUE;
const Bool_t excludeM4     = kTRUE;
const Bool_t TOFcorrection = kTRUE;
//____________________________________________________________________________________________________________________________________
void runGRID(const TString mode = "terminate_final", const Int_t pThardbin = -1)
{
  //mode should be test/full/terminate/terminate_final

  AliLog::SetGlobalLogLevel(AliLog::kError);

  TGrid::Connect("alien://");

  if(pThardbin > 0) kJJMC = kTRUE;

  gSystem->AddIncludePath("-I$ROOTSYS");
  gSystem->AddIncludePath("-I$ROOTSYS/include");
  gSystem->AddIncludePath("-I$ALICE_ROOT");
  gSystem->AddIncludePath("-I$ALICE_ROOT/include");
  gSystem->AddIncludePath("-I$ALICE_PHYSICS");
  gSystem->AddIncludePath("-I$ALICE_PHYSICS/include");
  gROOT->LoadMacro("AliAnalysisTaskPHOSSingleSim.cxx++g");
  
  // Create and configure the alien handler plugin
  AliAnalysisGrid *alienHandler = 0x0;
  alienHandler = CreateAlienHandler(mode,pThardbin);
  if(!alienHandler) return;

  AliAnalysisManager *mgr  = new AliAnalysisManager("Manager", "Manager");
  mgr->SetGridHandler(alienHandler);
  
  //MC handler
  if(kMC && kInputData.Contains("ESD")){
    AliMCEventHandler* mcHandler = new AliMCEventHandler();
    mcHandler->SetReadTR(kFALSE);//Do not search TrackRef file
    mgr->SetMCtruthEventHandler(mcHandler);
  }
 
  //input
  if(kInputData == "ESD"){
    // ESD handler
    AliESDInputHandler *esdHandler = new AliESDInputHandler();
    esdHandler->SetReadFriends(kFALSE);
    mgr->SetInputEventHandler(esdHandler);
  }
  else if(kInputData.Contains("AOD")){
    // AOD handler
    AliAODInputHandler *aodHandler = new AliAODInputHandler();
    mgr->SetInputEventHandler(aodHandler);
  }
  else{
    printf("input handler is neither ESD nor AOD. stop.\n");
    return;
  }
 
  //add necessary tasks.

//  //Physics selection
//  const Bool_t enablePileupCuts = kTRUE;
//  gROOT->LoadMacro("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
//  AliPhysicsSelectionTask* physSelTask = AddTaskPhysicsSelection(kMC, enablePileupCuts);

//  if(kCollision=="PbPb" || kCollision=="pPb" || kCollision=="Pbp"){
//    // Centrality for run2 for both ESD and AOD
//    gROOT->LoadMacro("$ALICE_PHYSICS/OADB/COMMON/MULTIPLICITY/macros/AddTaskMultSelection.C");
//    AliMultSelectionTask * task = AddTaskMultSelection(kFALSE); // user mode
//  }

  ////PID task for electron ID
  //gROOT->LoadMacro("$ALICE_ROOT/ANALYSIS/macros/AddTaskPIDResponse.C");
  //AddTaskPIDResponse(kMC);

  if(FlowTask){
    //for event plane
    gSystem->AddIncludePath("-I$ALICE_PHYSICS/include");

    gSystem->Load("libPWGPPevcharQn.so");
    gSystem->Load("libPWGPPevcharQnInterface.so");

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGPP/EVCHAR/FlowVectorCorrections/QnCorrectionsInterface/macros/runAnalysis.H");
    gROOT->LoadMacro("$ALICE_PHYSICS/PWGPP/EVCHAR/FlowVectorCorrections/QnCorrectionsInterface/macros/loadRunOptions.C");
    if (!loadRunOptions(kFALSE, ".")) {
      cout << "ERROR: configuration options not loaded. ABORTING!!!" << endl;
      return;
    }
    //only basic Qn correction
    //gROOT->LoadMacro("$ALICE_PHYSICS/PWGPP/EVCHAR/FlowVectorCorrections/QnCorrectionsInterface/macros/AddTaskFlowQnVectorCorrections.C");
    //AliAnalysisDataContainer *corrTask = AddTaskFlowQnVectorCorrections();

    //additional Qn correction
    gROOT->LoadMacro("$ALICE_PHYSICS/PWGPP/EVCHAR/FlowVectorCorrections/QnCorrectionsInterface/macros/AddTaskFlowQnVectorCorrectionsNewDetConfig.C");
    AliAnalysisDataContainer *corrTask = AddTaskFlowQnVectorCorrectionsNewDetConfig();

    //only for lego train
    //gROOT->LoadMacro("$ALICE_PHYSICS/PWGPP/EVCHAR/FlowVectorCorrections/QnCorrectionsInterface/macros/AddTaskFlowQnVectorCorrectionsToLegoTrain.C");
    //AddTaskFlowQnVectorCorrectionsToLegoTrain(".");
  }


  if(usePHOSTender){
    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    AliPHOSTenderTask *tender = AddAODPHOSTender("PHOSTenderTask","PHOStender","Run2Default",1,kMC);

    AliPHOSTenderSupply *supply = tender->GetPHOSTenderSupply();
    if(kMC){
      supply->ApplyZeroSuppression(0.020);
    }

    Char_t BadMap[128];
    //sprintf(BadMap,"%s","alien:///alice/cern.ch/user/d/dsekihat/BadMap/BadMap_empty.root");
    //supply->ForceUsingBadMap(BadMap);

//    if(period=="LHC15n"){
//      sprintf(BadMap,"%s","alien:///alice/cern.ch/user/d/dsekihat/BadMap/BadMap_LHC15n_v3.root");
//      supply->ForceUsingBadMap(BadMap);
//    }
//    else if(period=="LHC15o"){
//      sprintf(BadMap,"%s","alien:///alice/cern.ch/user/d/dsekihat/BadMap/BadMap_LHC15o_v3.root");
//      supply->ForceUsingBadMap(BadMap);
//    }
//    else if(period=="LHC16q" || period=="LHC16t"){
//      sprintf(BadMap,"%s","alien:///alice/cern.ch/user/d/dsekihat/BadMap/BadMap_LHC16qt.root");
//      supply->ForceUsingBadMap(BadMap);
//    }

  }

  gROOT->LoadMacro("AddTaskPHOSSingleSim.C");  
  AliAnalysisTaskPHOSSingleSim *ana_pi0   = AddTaskPHOSSingleSim("SingleSim","Pi0");
  AliAnalysisTaskPHOSSingleSim *ana_eta   = AddTaskPHOSSingleSim("SingleSim","Eta");
  AliAnalysisTaskPHOSSingleSim *ana_gamma = AddTaskPHOSSingleSim("SingleSim","Gamma");


/*
  Double_t bs = 25.;//in unit of ns
  if(kCollision=="PbPb") bs = 100.;
  else if(kCollision=="pPb")  bs = 100.;
  const Double_t distanceBC = 0.0;//in unit of cm

  gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_Run2/macros/AddTaskPHOSObjectCreator.C");
  AliAnalysisTaskPHOSObjectCreator *creator_bs25ns_dbc00cm = AddTaskPHOSObjectCreator("PHOSObjectCreator",AliVEvent::kAny,usePHOSTender,kMC,bs,0,NonLinCorr,excludeM4,period);

  Bool_t useCoreE = kFALSE;
  Bool_t useCoreDisp = kFALSE;
  const Int_t L1PHH = 7;
  const Int_t L1PHM = 6;
  const Int_t L1PHL = 5;
  const Int_t L0    = 9;

  Double_t Nsigma_Disp0 = 2.5;//default
  Double_t Nsigma_Disp1 = 2.0;//for systematic uncertainty
  Double_t Nsigma_Disp2 = 3.0;//for systematic uncertainty

  const Int_t Ndisp = 4;
  Double_t Nsigma_Disp[Ndisp] = {-1,2.5,2.0,3.0};
  const Int_t Ncpv  = 4;
  Double_t Nsigma_CPV[Ncpv]  = {-1,2.5,2.0,3.0};

  Double_t Nsigma_CPV0 = 2.5;//default
  Double_t Nsigma_CPV1 = 2.0;//for systematic uncertainty
  Double_t Nsigma_CPV2 = 3.0;//for systematic uncertainty

  gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_Run2/macros/AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV.C");
  gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_Run2/macros/AddTaskPHOSPi0EtaToGammaGamma_PbPb_5TeV.C");

  if(kCollision=="pp"){
    useCoreE    = kFALSE;
    useCoreDisp = kTRUE;
  }
  else if(kCollision=="pPb"){
    useCoreE    = kFALSE;
    useCoreDisp = kTRUE;
  }
  else if(kCollision=="PbPb"){
    useCoreE    = kTRUE;
    useCoreDisp = kTRUE;
  }

  TString triggerinput = "";
  if(kCollision=="pp"){
    const Float_t centrality[] = {0,9999};
    const Int_t Ncen = 2;
    const Int_t Nmix[Ncen-1] = {200};

    for(Int_t icen=0;icen<Ncen-1;icen++){
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_noPID = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[0],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_CPV = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[1],Nsigma_Disp[0],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_Disp = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[1],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_CPV_Disp = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[1],Nsigma_Disp[1],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);
    }//end of centrality loop

    if(period.Contains("LHC15n") && !kMC){
      triggerinput = "L0";

      for(Int_t icen=0;icen<Ncen-1;icen++){
        AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_PHI7_noPID = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kPHI7,kCollision,kMC,triggerinput,centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[0],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);
        AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_PHI7 = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kPHI7,kCollision,kMC,triggerinput,centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[1],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);

      }//end of centrality loop

    }

    ////only for non-linearity
    //useCoreE    = kTRUE;
    //for(Int_t icen=0;icen<Ncen-1;icen++){
    //  AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_noPID_coreE = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[0],usePHOSTender,bs,distanceBC,kJJMC,MCtype);
    //  AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_CPV_coreE = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[1],Nsigma_Disp[0],usePHOSTender,bs,distanceBC,kJJMC,MCtype);
    //  AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_Disp_coreE = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[1],usePHOSTender,bs,distanceBC,kJJMC,MCtype);
    //  AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_CPV_Disp_coreE = AddTaskPHOSPi0EtaToGammaGamma_pp_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[1],Nsigma_Disp[1],usePHOSTender,bs,distanceBC,kJJMC,MCtype);
    //}//end of centrality loop

  }
  else if(kCollision=="pPb"){
    const Float_t centrality[] = {0,10,30,50,90};
    const Int_t Ncen = 5;
    const Int_t Nmix[Ncen-1] = {10,20,50,100};

    for(Int_t icen=0;icen<Ncen-1;icen++){
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_noPID = AddTaskPHOSPi0EtaToGammaGamma("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[0],usePHOSTender,bs,distanceBC,kJJMC,MCtype);

      for(Int_t icpv=1;icpv<Ncpv;icpv++){
        for(Int_t idisp=1;idisp<Ndisp;idisp++){
          AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7 = AddTaskPHOSPi0EtaToGammaGamma("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[icpv],Nsigma_Disp[idisp],usePHOSTender,bs,distanceBC,kJJMC,MCtype);
        }
      }
    }//end of centrality loop

  }
  else if(kCollision=="PbPb"){
    const Float_t centrality[] = {0,10,30,50,90};
    const Int_t Ncen = 5;
    const Int_t Nmix[Ncen-1] = {10,20,50,100};
    for(Int_t icen=0;icen<Ncen-1;icen++){
      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_INT7_CPV_Disp = AddTaskPHOSPi0EtaToGammaGamma_PbPb_5TeV("Pi0EtaToGG",AliVEvent::kINT7,kCollision,kMC,triggerinput, centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[1],Nsigma_Disp[1],usePHOSTender,TOFcorrection,bs,distanceBC,kJJMC,MCtype);

    }//end of centrality loop

  }


//  if(period.Contains("LHC15o") && !kMC){
//    triggerinput = "L1H";
//    for(Int_t icen=0;icen<Ncen-1;icen++){
//      AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_PHI7 = AddTaskPHOSPi0EtaToGammaGamma("Pi0EtaToGG",AliVEvent::kPHI7,kCollision,kMC,triggerinput,centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[0],Nsigma_Disp[0],usePHOSTender,bs,distanceBC,kJJMC);
//      for(Int_t icpv=1;icpv<Ncpv;icpv++){
//        for(Int_t idisp=1;idisp<Ndisp;idisp++){
//          AliAnalysisTaskPHOSPi0EtaToGammaGamma *ana_PHI7 = AddTaskPHOSPi0EtaToGammaGamma("Pi0EtaToGG",AliVEvent::kPHI7,kCollision,kMC,triggerinput,centrality[icen],centrality[icen+1],Nmix[icen],FlowTask,useCoreE,useCoreDisp,Nsigma_CPV[icpv],Nsigma_Disp[idisp],usePHOSTender,bs,distanceBC,kJJMC);
//
//        }
//      }
//    }//end of centrality loop
//  }
*/

  //-----------------------
  // Run the analysis
  //-----------------------    
  mgr->InitAnalysis();
  mgr->PrintStatus();
  if(mode=="test") mgr->SetDebugLevel(2);
  else             mgr->SetDebugLevel(0);

  mgr->StartAnalysis("grid");
 
  printf("==================== runGRID.C is done ! ====================\n");
 
}
//____________________________________________________________________________________________________________________________________
AliAnalysisGrid* CreateAlienHandler(const TString mode, const Int_t pThardbin)
{
  gROOT->LoadMacro("SetGoodRuns.C"); 
  AliAnalysisAlien *plugin = new AliAnalysisAlien();

  if(mode=="terminate_final") plugin->SetMergeViaJDL(kFALSE);
  else                        plugin->SetMergeViaJDL(kTRUE);

  plugin->SetRunMode(mode);
  plugin->SetAliPhysicsVersion("vAN-20170620-1");
  // plugin->SetAliPhysicsVersion("vAN-20171008-1");

  TString WorkDir = "";
  if(MCname=="")      WorkDir = Form("Run2/%s/v102_%s_%s/",period.Data(),pass.Data(),kInputData.Data());
  else{
    if(pThardbin > 0) WorkDir = Form("Run2/%s/v102_%s_%s/pThardbin%d/",period.Data(),MCname.Data(),kInputData.Data(),pThardbin);
    else              WorkDir = Form("Run2/%s/v102_%s_%s/",period.Data(),MCname.Data(),kInputData.Data());
  }
  //Set Output Dir
  plugin->SetDefaultOutputs(kTRUE);
  //plugin->SetDefaultOutputs(kFALSE);
  //plugin->SetOutputFiles("AnalysisResults.root");

  //plugin->SetMergeExcludes("CalibrationHistograms.root");

  plugin->SetGridWorkingDir(WorkDir);
  plugin->SetGridOutputDir("output"); // In this case will be $HOME/work/output

  SetGoodRuns(plugin,kInputData,period,pass,MCname,pThardbin);

  plugin->AddIncludePath("-I.");
  plugin->AddIncludePath("-I$ROOTSYS/include");
  plugin->AddIncludePath("-I$ALICE_ROOT/include");
  plugin->AddIncludePath("-I$ALICE_PHYSICS/include");

  plugin->SetAnalysisSource("AliAnalysisTaskPHOSSingleSim.cxx");
  plugin->SetAdditionalLibs("AliAnalysisTaskPHOSSingleSim.cxx AliAnalysisTaskPHOSSingleSim.h");


  if(usePAR){
    //cp /data/dsekihat/alice/sw/BUILD/AliPhysics-latest-master/AliPhysics/PWGGA/PHOSTasks/PWGGAPHOSTasks.par .
    plugin->SetupPar("PWGGAPHOSTasks");
    plugin->EnablePackage("PWGGAPHOSTasks.par"); 
  }

  TString macroname = "";
  if(MCname=="") macroname = Form("TaskPHOSPi0EtaToGG_%s_%s_%s",period.Data(),pass.Data(),kInputData.Data());
  else{
    if(pThardbin > 0) macroname = Form("TaskPHOSPi0EtaToGG_%s_%s_pThardbin%d",MCname.Data(),kInputData.Data(),pThardbin);
    else              macroname = Form("TaskPHOSPi0EtaToGG_%s_%s",MCname.Data(),kInputData.Data());
  }

  //Set Job
  plugin->SetExecutableCommand("aliroot -b -q");
  plugin->SetAnalysisMacro(Form("%s.C",macroname.Data()));
  plugin->SetExecutable(Form("%s.sh",macroname.Data()));
  plugin->SetNtestFiles(1);
  plugin->SetTTL(36000);//10h * 3600s
  plugin->SetOutputToRunNo();
  plugin->SetCheckCopy(kFALSE);
  plugin->SetSplitMaxInputFileNumber(10);//10 only for embedding jobs //30 for LHC16q

  plugin->SetMaxMergeFiles(50);
  plugin->SetDropToShell(kFALSE);//log out from alien right after submitting jobs.

  plugin->SetInputFormat("xml-single");
  plugin->SetJDLName(Form("%s.jdl",macroname.Data()));
  plugin->SetPrice(1);      
  plugin->SetSplitMode("se");
  return plugin;

}
//____________________________________________________________________________________________________________________________________

