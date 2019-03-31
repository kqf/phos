#include "../../setup/environment.h"
#include "../../setup/tender.h"
#include "plugin.h"
#include <PWGGA/PHOSTasks/PHOS_LHC16_pp/macros/AddAnalysisTaskPP.C>
// #include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL, isMC));
    manager->SetInputEventHandler(new AliAODInputHandler());

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    TString msg = message("Real data", period);
    AddPHOSTender(isMC, msg);

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

    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(isMC, msg);
    task->SelectCollisionCandidates(AliVEvent::kINT7);
    AddTaskPHOSEpRatio(isMC);

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}
