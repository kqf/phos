#include "../../../setup/environment.h"
#include "../../../tasks/analysis-task-pp/macros/AddAnalysisTaskPP.C"
#include "plugin.h"
#include <PWGGA/PHOSTasks/PHOS_LHC16_pp/macros/AddAnalysisAcceptanceTaskPP.C>

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();

    manager->SetInputEventHandler(aod);

    if(isMC)
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR(kFALSE); // Don't read track references
        manager->SetMCtruthEventHandler( mchandler );
    }

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC

    TString pref =  isMC ? "MC" : "";
    TString tenderOption = isMC ? "Run2Tuned" : "Run2TunedMC";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    // PHOSSupply->ForceUsingBadMap("../../../datasets/BadMap_LHC16-updated.root");

    AliAnalysisTaskPIDResponse *taskPID = AddTaskPIDResponse(
            isMC,
            kTRUE,
            kTRUE,
            1,          // reco pass
            kFALSE,
            "",
            kTRUE,
            kFALSE,
            1           // reco pass
                                          );

    if(isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }

    TString msg = "## Real data, no TOF cut efficiency.";
    if(tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    // AddTaskPHOSEpRatio(isMC);
    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(isMC, period + pref + msg);

    task->SelectCollisionCandidates(AliVEvent::kINT7);
    AddTaskPHOSEpRatio(isMC);

    AliAnalysisTaskPP13 * task2 = AddAnalysisAcceptanceTaskPP(isMC, period + pref + msg);
    task2->SelectCollisionCandidates(AliVEvent::kINT7);


    if(!manager->InitAnalysis()) return;
    manager->PrintStatus();


    alien->SetOutputFiles("AnalysisResults.root");
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
