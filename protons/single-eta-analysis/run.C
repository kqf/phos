#include "../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL);

    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();
    manager->SetInputEventHandler(aod);
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC

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

    // Configure Tender
    AliPHOSTenderSupply * supply = tender->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../datasets/BadMap_LHC16-updated.root");
    
    Double_t zs_threshold = 0.020; // ZS threshold in unit of GeV
    supply->ApplyZeroSuppression(zs_threshold);


    gROOT->LoadMacro("../setup/values_for_dataset.h+");
    std::vector<Int_t> cells;
    values_for_dataset(cells, "BadCells_LHC16", "../datasets/");
    // There is no need to download QA when we use don't use JDL
    // if (useJDL)

    TString msg = "Single #eta Analysis + weights iteration 0";
    msg += " with tender option ";
    msg += decalibration;


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