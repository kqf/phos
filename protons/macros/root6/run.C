#ifdef __CLING__

// Tell ROOT where to find AliPhysics headers
R__ADD_INCLUDE_PATH($ALICE_PHYSICS)
#include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
#include <OADB/macros/AddTaskPhysicsSelection.C>
#include <PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C>
#include <PWGGA/PHOSTasks/PHOS_EpRatio/AddTaskPHOSEpRatio.C>
#endif

#include "../../setup/environment.h"

void run(TString period, const char * runmode = "local", const char * pluginmode = "test", TString dpart = "first", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.cc+");
    AliAnalysisGrid * alien = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");
    AliAODInputHandler * aod = new AliAODInputHandler();
}
