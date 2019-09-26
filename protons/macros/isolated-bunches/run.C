#include "../../setup/environment.h"
#include "../../setup/tender.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL, isMC));
    manager->SetInputEventHandler(new AliAODInputHandler());

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC

    TString msg = message("Isolated photons no timing cut", period);
    AddPHOSTender(isMC, msg);

    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(msg, period);
    task->SelectCollisionCandidates(AliVEvent::kINT7);

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
