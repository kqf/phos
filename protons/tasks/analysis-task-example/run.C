#include "../../setup/environment.h"
#include "AliAnalysisTaskPi0v4.cxx"
#include "task.h"

void run(const char * runmode = "local", const char * pluginmode = "test", bool mergeJDL = kTRUE, bool isMC = kFALSE)
{
    SetupEnvironment();

    bool useTender = kTRUE;
    // TString period = "LHC16h";
    TString period = "LHC16k";
    Int_t * good_runs;
    Int_t nruns;

    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, period, dpart, useJDL, isMC);
    if (!alienHandler) return;

    AliAnalysisManager * mgr  = new AliAnalysisManager("PHOS_Pi0_Spectrum");
    AliESDInputHandler * esdH = new AliESDInputHandler();
    AliAODInputHandler * aodH = new AliAODInputHandler();

    esdH->SetReadFriends( isMC );
    // mgr->SetInputEventHandler( esdH );
    mgr->SetInputEventHandler( aodH );
    esdH->SetNeedField();

    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Not reading track references
        mgr->SetMCtruthEventHandler ( mchandler );
    }

    // Connect plug-in to the analysis manager
    mgr->SetGridHandler(alienHandler);
    // mgr->SetDebugLevel(999999);
    AddTaskPhysicsSelection ( isMC, kTRUE, 0, kTRUE);  //false for data, kTRUE for MC


    // Add task without tender
    // Tender doesn't allow us to run the macro before and after TENDER Task
    if (!useTender) AddMyTask(AliVEvent::kINT7, "None", "NoTender", "BadMap_LHC16k.root");;

    // Add tender
    if (useTender)
    {
        AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
        AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
        PHOSSupply->ForceUsingBadMap("BadMap_LHC16k.root");

        AddMyTask(AliVEvent::kINT7, "None", "WithTender", "");
        // AddMyTask(AliVEvent::kINT7, "LHC16i ## only my(!) badmap in tender ## only tender", "OnlyTender");
    }

    if ( !mgr->InitAnalysis( ) ) return;
    // mgr->PrintStatus();


    mgr->StartAnalysis (runmode);
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
