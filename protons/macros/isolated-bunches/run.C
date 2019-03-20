#include "../../setup/environment.h"
#include "plugin.h"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    // SetupEnvironment();

    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();

    manager->SetInputEventHandler(aod);

    if(isMC)
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR(kFALSE); // Don't read track references
        manager->SetMCtruthEventHandler(mchandler);
    }

    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alien);


    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection(isMC, enablePileupCuts);  //false for data, true for MC


    TString tenderOption = isMC ? "Run2Default" : "";
    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender", tenderOption, 1, isMC);

    AliPHOSTenderSupply * supply = tenderPHOS->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    TString nonlinearity = isMC ? "Run2Tune" : "Run2TuneMC";
    supply->SetNonlinearityVersion(nonlinearity); 


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

    if(isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        supply->ApplyZeroSuppression(zs_threshold);
    }

    TString msg = "## Real data, no TOF cut efficiency.";
    if(tenderOption)
    {
        msg += " with tender option ";
        msg += tenderOption;
    }

    Bool_t isTest = TString(pluginmode).Contains("test");
    TString pref =  isMC ? "MC" : "";

    AddAnalysisTaskPP(AliVEvent::kINT7, period + pref + msg, period,isMC, isTest);
    manager->InitAnalysis();
    manager->PrintStatus();

    TString files = AliAnalysisManager::GetCommonFileName();
    cout << "Output files " << files << endl;
    alien->SetOutputFiles(files);

    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
