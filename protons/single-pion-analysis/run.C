#include "../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL);

    AliAODInputHandler * aod = new AliAODInputHandler();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");

    manager->SetInputEventHandler(aod);
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection(
        kTRUE,             //false for data, true for MC
        enablePileupCuts
    );

    // NB: This is a local copy of steering macro
    gROOT->LoadMacro("AddAnalysisTaskPP.C");

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");

    TString decalibration = "Run2Default";
    AliPHOSTenderTask * tender = AddAODPHOSTender(
        "PHOSTenderTask",  // Task Name
        "PHOStender",      // Container Name
        decalibration,     // Important: de-calibration
         1,                // Important: reco pass 
         kTRUE             // Important: is MC?
    );

    AliPHOSTenderSupply * supply = tender->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");

    // ZS threshold in unit of GeV
    Double_t zs_threshold = 0.020;
    supply->ApplyZeroSuppression(zs_threshold);


    gROOT->LoadMacro("../setup/values_for_dataset.h+");
    std::vector<Int_t> cells;
    values_for_dataset(cells, "BadCells_LHC16", "../datasets/");


    TString msg = "Single pion analysis + weights iteration 2";
    msg += " with tender option ";
    msg += decalibration;

    TString pref = "MC";
    AddAnalysisTaskPP(period + pref + msg, "Tender", "", cells);
    AddAnalysisTaskPP(period + pref + msg, "OnlyTender", "", std::vector<Int_t>());
    manager->InitAnalysis();
    manager->PrintStatus();

    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    alien->SetOutputFiles(files);

    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}