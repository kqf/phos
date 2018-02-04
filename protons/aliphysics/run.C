// #include "../setup/sources.h"

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
    gROOT->LoadMacro("CreatePlugin.cc+");

    AliAnalysisManager * manager  = new AliAnalysisManager("PHOS_PP");

    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        manager->SetMCtruthEventHandler ( mchandler );
    }
    // Connect plug-in to the analysis manager
    manager->SetGridHandler(alienHandler);

    AliAODInputHandler * aodH = new AliAODInputHandler();
    manager->SetInputEventHandler(aodH);

    // LoadAnalysisLibraries(); // Local tests
    // gROOT->LoadMacro("AddAnalysisTaskPP.C"); // Local tests

    gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_LHC16_pp/macros/AddAnalysisTaskPP.C");
    TString pref =  isMC ? "MC" : "";
    AddAnalysisTaskPP(isMC, "test");

    if ( !manager->InitAnalysis( ) ) return;
    
    manager->PrintStatus();
    alienHandler->SetOutputFiles("AnalysisResults.root");
    manager->StartAnalysis (runmode);
    gObjectTable->Print( );
}

void SetupEnvironment()
{
    // ROOT
    gSystem->Load ( "libCore.so" );
    gSystem->Load ( "libGeom.so" );
    gSystem->Load ( "libVMC.so" );
    gSystem->Load ( "libPhysics.so" );
    gSystem->Load ( "libTree.so" );
    gSystem->Load ( "libMinuit.so" );

    // AliROOT
    gSystem->Load ( "libSTEERBase.so" );
    gSystem->Load ( "libESD.so" );
    gSystem->Load ( "libAOD.so" );
    gSystem->Load ( "libANALYSIS.so" );
    gSystem->Load ( "libANALYSISalice.so" );
    gSystem->Load ( "libPWGGAPHOSTasks.so" );

    // Tender
    gSystem->Load("libTender.so");
    gSystem->Load("libTenderSupplies.so");
    gSystem->Load("libPWGGAPHOSTasks.so");

    // for running with root only
    gSystem->Load( "libTree.so" );
    gSystem->Load( "libGeom.so" );
    gSystem->Load( "libVMC.so" );
    gSystem->Load( "libPhysics.so" );

    //add include path
    gSystem->AddIncludePath( "-I$ALICE_ROOT/include" );
    gSystem->AddIncludePath( "-I$ALICE_PHYSICS/include" );
    gSystem->SetMakeSharedLib(TString(gSystem->GetMakeSharedLib()).Insert(19, " -Wall ") );
}

