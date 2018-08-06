#include "../../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);

    AliAODInputHandler * aod = new AliAODInputHandler();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");

    manager->SetInputEventHandler(aod);
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection(
        kTRUE,             //false for data, true for MC
        enablePileupCuts
    );

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    TString decalibration = "Run2Default";
    AliPHOSTenderTask * tender = AddAODPHOSTender(
                                     "PHOSTenderTask",  // Task Name
                                     "PHOStender",      // Container Name
                                     "",                // Important: de-calibration
                                     1,                 // Important: reco pass
                                     isMC              // Important: is MC?
                                 );
    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_TriggerQA/macros/AddTaskPHOSTriggerQA.C");
    AddTaskPHOSTriggerQA(AliAnalysisManager::GetCommonFileName());
  
    // AddAnalysisTaskPP(period + pref + msg, "OnlyTender", "", std::vector<Int_t>());
    manager->InitAnalysis();
    manager->PrintStatus();

    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    alien->SetOutputFiles(files);

    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}