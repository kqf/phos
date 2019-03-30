#include "../../setup/environment.h"
#include "../../setup/tender.h"
#include "plugin.h"
// #include "task.h"
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
    AddTaskPhysicsSelection(isMC, enablePileupCuts);

    TString msg = "Nonlinearity Scan";
    msg += " AliPhysics version:";
    msg += gSystem->Getenv("ALIPHYSICS_VERSION");
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
