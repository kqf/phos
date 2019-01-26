#include "../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);

    if (!alienHandler) return;

    AliAnalysisManager * mgr  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aodH = new AliAODInputHandler();

    mgr->SetInputEventHandler(aodH);

    AliMCEventHandler * mchandler = new AliMCEventHandler();
    mchandler->SetReadTR ( kFALSE ); // Don't read track references
    mgr->SetMCtruthEventHandler ( mchandler );

    // Connect plug-in to the analysis manager
    mgr->SetGridHandler(alienHandler);

 

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

 

    TString pref =  isMC ? "MC" : "";

 

    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    PHOSSupply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");
    PHOSSupply->ForceUsingCalibration("../datasets/Calib2016Time2017.root");

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }

    TString msg = "## Real data, no TOF cut efficiency, different time callibration";

    if (tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    Bool_t isTest = TString(pluginmode).Contains("test");
    AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, "Tender", "", isMC, isTest);


    if ( !mgr->InitAnalysis( ) ) return;
    mgr->PrintStatus();


    alienHandler->SetOutputFiles("AnalysisResults.root");
    mgr->StartAnalysis (runmode);
    gObjectTable->Print( );
}
