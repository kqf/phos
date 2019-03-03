#include "../../setup/environment.h"
#include "plugin.h"
// #include "task.h"


void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    alien->SetOutputFiles("TriggerQA.root");

    AliAODInputHandler * aod = new AliAODInputHandler();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");

    manager->SetInputEventHandler(aod);
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(
        isMC,             //false for data, true for MC
        enablePileupCuts
    );


    AliPHOSTenderTask * tender = AddAODPHOSTender(
                                     "PHOSTenderTask",  // Task Name
                                     "PHOStender",      // Container Name
                                     "",                // Important: de-calibration
                                     1,                 // Important: reco pass
                                     isMC              // Important: is MC?
                                 );
    AliAnalysisTaskPHOSTriggerQA * task = AddTaskPHOSTriggerQA("TriggerQA.root", "PHOSTriggerQAResultsL0");
    // AliAnalysisTaskPHOSTriggerQAv1 * task = AddTaskPHOSTriggerQAv1(
    //     TString("TriggerQA.root"),
    //     "PHOSTriggerQAResultsL0"
    // );
    task->SelectCollisionCandidates(AliVEvent::kPHI7);

  
    // AddAnalysisTaskPP(period + pref + msg, "OnlyTender", "", std::vector<Int_t>());
    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    
    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
