#include "../../../setup/environment.h"
#include <PWGGA/PHOSTasks/PHOS_LHC16_pp/macros/AddAnalysisTaskPP.C>
// #include "../../../tasks/analysis-task-pp/macros/AddAnalysisTaskPP.C"
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
    SetupEnvironment();

    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");

    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        manager->SetMCtruthEventHandler ( mchandler );
    }
    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    AliAODInputHandler * aodH = new AliAODInputHandler();
    manager->SetInputEventHandler(aodH);


    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC



    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);
    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    // AliAnalysisTaskPIDResponse *taskPID = AddTaskPIDResponse(
    //     isMC, 
    //     kTRUE,
    //     kTRUE, 
    //     1,          // reco pass
    //     kFALSE, 
    //     "",
    //     kTRUE,
    //     kFALSE,
    //     1           // reco pass
    // );

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }
    TString pref =  isMC ? "MC" : "";
    AddAnalysisTaskPP(isMC, "test");

    if ( !manager->InitAnalysis( ) ) return;
    
    manager->PrintStatus();
    alienHandler->SetOutputFiles("AnalysisResults.root");
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}
