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

    TString decalibration = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tender = AddAODPHOSTender(
        "PHOSTenderTask",  // Task Name
        "PHOStender",      // Container Name
        decalibration,     // Important: de-calibration
        1,                 // Important: reco pass
        isMC               // Important: is MC?
     );

    AliPHOSTenderSupply * supply = tenderPHOS->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    TString nonlinearity = isMC ? "Run2Tune" : "Run2TuneMC";
    supply->SetNonlinearityVersion(nonlinearity);  

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }


    AliAnalysisTaskPHOSTriggerQA * task = AddTaskPHOSTriggerQA(
        "TriggerQA.root",
        "PHOSTriggerQAResultsL0"
    );

    task->SelectCollisionCandidates(AliVEvent::kPHI7);
    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
