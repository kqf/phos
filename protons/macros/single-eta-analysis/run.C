#include "../../setup/environment.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kTRUE, Bool_t useJDL = kTRUE)
{
    // SetupEnvironment();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    manager->SetGridHandler(CreatePlugin(pluginmode, period, dpart, useJDL));
    manager->SetInputEventHandler(new AliAODInputHandler());

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(
        kTRUE,  //false for data, true for MC
        enablePileupCuts
    );

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
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    Double_t zs_threshold = 0.020; // ZS threshold in unit of GeV
    supply->ApplyZeroSuppression(zs_threshold);

    TString nonlinearity = isMC ? "Run2Tune" : "Run2TuneMC";
    supply->SetNonlinearityVersion(nonlinearity); 


    TString msg = "Tuned nonlinearity";
    msg += " with tender option: ";
    msg += decalibration;
    msg += " AliPhysics version:";
    msg += gSystem->Getenv("ALIPHYSICS_VERSION");
    TString pref = "MC";

    // NB: This is a local copy of steering macro
    AliAnalysisTaskPP13 * task = AddAnalysisTaskPP(period + pref + msg, kTRUE);
    // Don't apply PhysicsSelection for SPMC
    // task->SelectCollisionCandidates(AliVEvent::kINT7);

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis(runmode);

    gObjectTable->Print();
}
