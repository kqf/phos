#ifdef __CLING__

R__ADD_INCLUDE_PATH($ALICE_ROOT)
#include <ANALYSIS/macros/AddTaskPIDResponse.C>

R__ADD_INCLUDE_PATH($ALICE_PHYSICS)
#include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
#include <OADB/macros/AddTaskPhysicsSelection.C>
#include <PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C>

#endif

#include "../../setup/environment.h"
#include "CreatePlugin.cc"
#include "AddAnalysisTaskPP.C"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();
    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        manager->SetMCtruthEventHandler ( mchandler );
    }

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alien);
    manager->SetInputEventHandler(aod);


    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    TString pref =  isMC ? "MC" : "";


    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    PHOSSupply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    AliAnalysisTaskPIDResponse *taskPID = AddTaskPIDResponse(
        isMC, 
        kTRUE,
        kTRUE, 
        1,          // reco pass
        kFALSE, 
        "",
        kTRUE,
        kFALSE,
        1           // reco pass
    );

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

    Bool_t isTest = TString(pluginmode).Contains("test");
    gInterpreter->ProcessLine("AddAnalysisTaskPP.C");
    AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, "", isMC, isTest);
    AddTaskPHOSEpRatio(isMC);


    if ( !manager->InitAnalysis( ) ) return;
    manager->PrintStatus();


    alien->SetOutputFiles("AnalysisResults.root");
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}
