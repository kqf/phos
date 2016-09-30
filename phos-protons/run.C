void run(const char * runmode = "local", const char * pluginmode = "test", bool isMC = false)
{
    SetupEnvironment();

    bool useTender = kFALSE;
    TString period = "LHC16h";
    Int_t * excells;
    Int_t * good_runs;
    Int_t nexc;
    Int_t nruns;
    gROOT->LoadMacro("../qa/getRunsBadCells.C");
    getRunsBadCells(period, good_runs, nruns, excells, nexc);




    gROOT->LoadMacro("CreatePlugin.C");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, good_runs, nruns, period);
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

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection ( isMC, kTRUE, 0, kTRUE);  //false for data, true for MC

    gROOT->LoadMacro("PhotonSelection.cxx+");
    gROOT->LoadMacro("TestPhotonSelection.cxx+");
    gROOT->LoadMacro("PhysPhotonSelection.cxx+");
    gROOT->LoadMacro("MixingSample.h+");
    gROOT->LoadMacro("AliAnalysisTaskPrompt.cxx+");
    gROOT->LoadMacro("AddMyTask.C");

    // Add task without tender
    // Tender doesn't allow us to run the macro before and after TENDER Task
    if (!useTender) AddMyTask(AliVEvent::kINT7, period + "## only my badmap ## no tender", "NoTender", "", excells, nexc);

    // Add tender
    if (useTender)
    {
        gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
        AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
        AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
        PHOSSupply->ForceUsingBadMap("BadMap_LHC16i.root");

        AddMyTask(AliVEvent::kINT7, "LHC16i ## my badmap + my(!) badmap in tender ## with tender", "WithTender", "BadMap_LHC16i.root");
        AddMyTask(AliVEvent::kINT7, "LHC16i ## only my(!) badmap in tender ## only tender", "OnlyTender");
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

