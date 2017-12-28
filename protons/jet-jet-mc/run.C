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

    esdH->SetReadFriends(isMC);
    esdH->SetNeedField();
    manager->SetInputEventHandler(aodH);

    AliMCEventHandler * mchandler = new AliMCEventHandler();
    mchandler->SetReadTR ( kFALSE ); // Don't read track references
    manager->SetMCtruthEventHandler ( mchandler );

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    gROOT->LoadMacro("AddAnalysisTaskPP.C");
    TString files = "";
    TString pref =  isMC ? "MC" : "";

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();

    // TODO: Move bad map outside this directory
    //

    PHOSSupply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        PHOSSupply->ApplyZeroSuppression(zs_threshold);
    }


    gROOT->LoadMacro("../datasets/values_for_dataset.h+");
    std::vector<Int_t> cells;
    values_for_dataset(cells, "BadCells_LHC16", "../datasets/");
    // There is no need to download QA when we use don't use JDL
    // if (useJDL)
    // files += AddTaskCaloCellsQAPt(AliVEvent::kINT7, cells);

    TString msg = "## Jet-Jet MC ## nonlinearity applied, 20 MeV Zero Supression ";

    if (tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    files += AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, "Tender", "", cells, isMC);
    AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, "OnlyTender", "", std::vector<Int_t>(), isMC);
    //files += AddAnalysisTaskTrackAverages(good_runs, nruns);


    if ( !manager->InitAnalysis( ) ) return;
    manager->PrintStatus();


    cout << "Downloading files " << files << endl;
    alienHandler->SetOutputFiles(files);
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}