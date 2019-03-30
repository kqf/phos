#include "../../setup/environment.h"
#include "../../setup/tender.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kTRUE, Bool_t useJDL = kTRUE)
{
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL));
    manager->SetInputEventHandler(new AliAODInputHandler());

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);

    TString msg = message("Acceptance scan", period);
    AddPHOSTender(isMC, msg);

    // NB: This is a local copy of steering macro
    Bool_t acceptance = kTRUE;
    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(msg, acceptance);
    // Don't apply PhysicsSelection for SPMC
    task->SelectCollisionCandidates(AliVEvent::kINT7);

    manager->InitAnalysis();
    manager->PrintStatus();
    // manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
