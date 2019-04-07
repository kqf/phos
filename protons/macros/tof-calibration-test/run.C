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

    TString msg = message("## Real data, no TOF cut efficiency, 2017 time callibration", period);

    AliPHOSTenderTask * tender = AddPHOSTender(isMC, msg);

    AliPHOSTenderSupply * supply = tender->GetPHOSTenderSupply();
    supply->ForceUsingCalibration("../../datasets/Calib2016Time2017.root");

    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(msg);
    task->SelectCollisionCandidates(AliVEvent::kINT7);

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print(); 
    SetupEnvironment();
}
