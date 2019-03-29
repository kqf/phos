#include "../../setup/environment.h"
#include "plugin.h"
// #include "task.h"


void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAODInputHandler * aod = new AliAODInputHandler();

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
    task->SelectCollisionCandidates(AliVEvent::kPHI7);
    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
