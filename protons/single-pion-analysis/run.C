#include "../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);

    if (!alienHandler) return;

    AliAnalysisManager * mgr  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aodH = new AliAODInputHandler();

    mgr->SetInputEventHandler(aodH);

    // if ( isMC )
    // {
    //     AliMCEventHandler * mchandler = new AliMCEventHandler();
    //     mchandler->SetReadTR ( kFALSE ); // Don't read track references
    //     mgr->SetMCtruthEventHandler ( mchandler );
    // }

    // Connect plug-in to the analysis manager
    mgr->SetGridHandler(alienHandler);

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC

    // NB: This is a local copy of steering macro
    gROOT->LoadMacro("AddAnalysisTaskPP.C");

    TString pref =  isMC ? "MC" : "";

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    TString tenderOption = isMC ? "Run2Default" : "";
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


    gROOT->LoadMacro("../setup/values_for_dataset.h+");
    std::vector<Int_t> cells;
    values_for_dataset(cells, "BadCells_LHC16", "../datasets/");
    // There is no need to download QA when we use don't use JDL
    // if (useJDL)

    TString msg = "Single pion analysis + weights iteration 2";

    if (tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    AddAnalysisTaskPP(period + pref + msg, "Tender", "", cells);
    AddAnalysisTaskPP(period + pref + msg, "OnlyTender", "", std::vector<Int_t>());
    if ( !mgr->InitAnalysis( ) ) return;
    mgr->PrintStatus();


    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    alienHandler->SetOutputFiles(files);

    mgr->StartAnalysis(runmode);
    gObjectTable->Print();
}