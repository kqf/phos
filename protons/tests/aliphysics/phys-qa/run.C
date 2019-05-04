#include "../../../setup/environment.h"
#include <PWGGA/PHOSTasks/CaloCellQA/phys/macros/AddTaskPhysPHOSQA.C>
#include "plugin.h"

void run(
    TString period,
    const char * runmode = "local",
    const char * pluginmode = "test",
    TString dpart = "first",
    Bool_t isMC = kFALSE,
    Bool_t useJDL = kTRUE
)
{
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL, isMC));
    manager->SetInputEventHandler(new AliAODInputHandler());    // Connect plug-in to the analysis manager

    AddTaskPhysPHOSQA();

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
