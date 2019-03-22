#include "../../../setup/environment.h"
#include "plugin.h"

void run(
    TString period,
    const char * runmode = "local",
    const char * pluginmode = "test",
    TString dpart = "first",
    Bool_t isMC = kFALSE,
    Bool_t useJDL = kTRUE
)
{
    SetupEnvironment();
    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");

    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    if(isMC)
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR(kFALSE); // Don't read track references
        manager->SetMCtruthEventHandler(mchandler);
    }
    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    AliAODInputHandler * aodH = new AliAODInputHandler();
    manager->SetInputEventHandler(aodH);

    TString pref =  isMC ? "MC" : "";
    AddTaskPhysPHOSQA();

    if(!manager->InitAnalysis())
        return;

    manager->PrintStatus();
    alienHandler->SetOutputFiles("CaloCellsQA.root");
    manager->StartAnalysis(runmode);
    gObjectTable->Print();
}
