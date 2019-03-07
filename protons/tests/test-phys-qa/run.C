#include "../../setup/environment.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();

    manager->SetInputEventHandler(aod);
    if (isMC)
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        manager->SetMCtruthEventHandler ( mchandler );
    }
    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alien);


    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC



    TString pref =  isMC ? "MC" : "";


    TString tenderOption = isMC ? "Run2Tune" : "Run2TuneMC";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    PHOSSupply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }



    TString msg = "## Real data, no TOF cut efficiency.";
    if (tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    AliAnalysisTaskCaloCellsPhysQA * task = AddTaskPhysPHOSQA();
    // TOOD: Fix this 
    // task->SetCollisionCandidates(AliVEvent::kINT7);


    if (!manager->InitAnalysis()) return;
    manager->PrintStatus();


    alien->SetOutputFiles("AnalysisResults.root");
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}
