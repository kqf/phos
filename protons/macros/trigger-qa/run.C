#include "../../setup/environment.h"
#include "../../setup/tender.h"
#include "plugin.h"


void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    manager->SetInputEventHandler(AliAODInputHandler());
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL, isMC));

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);

    TString msg = message("Trigger QA", period);
    AddPHOSTender(isMC, msg);

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
