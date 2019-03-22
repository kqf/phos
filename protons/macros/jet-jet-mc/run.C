#include "../../setup/environment.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);

    if(!alienHandler) return;

    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aodH = new AliAODInputHandler();
    manager->SetInputEventHandler(aodH);

    AliMCEventHandler * mcHandler = new AliMCEventHandler();
    mcHandler->SetReadTR(kFALSE); // Don't read track references
    manager->SetMCtruthEventHandler(mcHandler);

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC

    TString pref =  isMC ? "MC" : "";

    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * supply = tenderPHOS->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    if(isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        supply->ApplyZeroSuppression(zs_threshold);
    }

    TString msg = "## Jet-Jet MC ## nonlinearity applied, 20 MeV Zero Supression ";
    if(tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(isMC, period + pref + msg);
    task->SetCollisionCandidates(AliVEvent::kINT7);

    if(!manager->InitAnalysis())
        return;

    manager->PrintStatus();
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
