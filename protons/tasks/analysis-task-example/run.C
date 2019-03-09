#include "../../setup/environment.h"
#include "AliAnalysisTaskPi0v4.cxx"
#include "task.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    AliAnalysisManager * manager = new AliAnalysisManager("PHOS_Pi0_Spectrum_Test");

    AliAODInputHandler * aod = new AliAODInputHandler();
    aod->SetReadFriends(isMC);
    aod->SetNeedField();
    manager->SetInputEventHandler(aod);

    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    manager->SetGridHandler(alien);

    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR(kFALSE); // Not reading track references
        manager->SetMCtruthEventHandler(mchandler);
    }

    Bool_t isPileup = kTRUE;
    AddTaskPhysicsSelection(isMC, isPileup);  //false for data, kTRUE for MC

    AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
    AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    PHOSSupply->ForceUsingBadMap("../../datasets/BadMap_LHC16.root");
    AddMyTask(AliVEvent::kINT7, "None", "WithTender", "");

    manager->InitAnalysis();
    manager->PrintStatus();
    manager->StartAnalysis (runmode);

    gObjectTable->Print();
}
