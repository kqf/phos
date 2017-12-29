#include "../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);

    if (!alienHandler) return;

    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    AliESDInputHandler * esdH = new AliESDInputHandler();
    AliAODInputHandler * aodH = new AliAODInputHandler();

    if (isMC)
    {
        esdH->SetReadFriends( isMC );
        esdH->SetNeedField();
        // manager->SetInputEventHandler( esdH );

    }
    // manager->SetInputEventHandler( esdH );
    manager->SetInputEventHandler(aodH);

    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        manager->SetMCtruthEventHandler ( mchandler );
    }

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    TString files = "";
    TString pref =  isMC ? "MC": "";

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    PHOSSupply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");


    gROOT->LoadMacro("$ALICE_ROOT/ANALYSIS/macros/AddTaskPIDResponse.C"); 
    AliAnalysisTaskPIDResponse *PIDResponse = AddTaskPIDResponse(isMC);
    PIDResponse->SelectCollisionCandidates(AliVEvent::kINT7);

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C");
    AddTaskPHOSEpRatio(isMC);

    // Important: Keep track of this variable
    // ZS threshold in unit of GeV  
    Double_t zs_threshold = 0.020;
    PHOSSupply->ApplyZeroSuppression(zs_threshold); 


    TString msg = "## Updated parameters for nonlinearity, 20 MeV Zero Supression ";

    if (tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    if ( !manager->InitAnalysis( ) ) return;
    manager->PrintStatus();


    cout << "Downloading files " << files << endl;
    alienHandler->SetOutputFiles(AliAnalysisManager::GetCommonFileName());
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}