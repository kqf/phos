#include "../../setup/environment.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kTRUE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL);

    AliAODInputHandler * aod = new AliAODInputHandler();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");

    manager->SetInputEventHandler(aod);
    manager->SetGridHandler(alien);

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(
        kTRUE,             //false for data, true for MC
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

    AliPHOSTenderSupply * supply = tender->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    // ZS threshold in unit of GeV
    Double_t zs_threshold = 0.020;
    supply->ApplyZeroSuppression(zs_threshold);

    TString nonlinearity = isMC ? "Run2Tune" : "Run2TuneMC";
    supply->SetNonlinearityVersion(nonlinearity); 

    TString msg = "Nonlinearity Scan";
    msg += " with tender option: ";
    msg += decalibration;
    msg += " AliPhysics version:";
    msg += " Nonlinearity version:";
    msg += nonlinearity;
    msg += gSystem->Getenv("ALIPHYSICS_VERSION");

    TString pref = "MC";

    // NB: This is a local copy of steering macro
    AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, "", "");

    manager->InitAnalysis();
    manager->PrintStatus();
    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    alien->SetOutputFiles(files);

    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
