void run(const char * runmode = "local", const char * pluginmode = "test", bool isMC = false)
{
    SetupEnvironment();

    gROOT->LoadMacro("CreatePlugin.C");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode);

    if (!alienHandler) return;

    AliAnalysisManager * mgr  = new AliAnalysisManager("PHOS_QA");
    AliESDInputHandler * esdH = new AliESDInputHandler();
    AliAODInputHandler * aodH = new AliAODInputHandler();

    // esdH->SetReadFriends( isMC );
    mgr->SetInputEventHandler(aodH);
    // mgr->SetInputEventHandler( esdH );
    // esdH->SetNeedField();

    if ( isMC )
    {
        AliMCEventHandler * mchandler = new AliMCEventHandler();
        mchandler->SetReadTR ( kFALSE ); // Not reading track references
        mgr->SetMCtruthEventHandler ( mchandler );
    }

    // Connect plug-in to the analysis manager
    mgr->SetGridHandler(alienHandler);

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection ( isMC );  //false for data, true for MC

    // Add tender
    // gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
    // AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
    // AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
    // PHOSSupply->ForceUsingBadMap("BadMap_LHC16i.root");
    // PHOSSupply->ForceUsingCalibration(0);
    // Force warnings !!!
    // gSystem->SetMakeSharedLib(TString(gSystem->GetMakeSharedLib()).Insert(19, " -Wall ") );
    // gROOT->LoadMacro("AliAnalysisTaskPi0QA.cxx+");

    // gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/CaloCellQA/macros/AddTaskPHOSQA.C");

    // AliAnalysisTaskSE * myTask = AddTaskPHOSQA();
    // myTask->SelectCollisionCandidates(AliVEvent::kINT7);

    gSystem->SetMakeSharedLib(TString(gSystem->GetMakeSharedLib()).Insert(19, " -Wall ") );
    gROOT->LoadMacro("AnalysisTaskCellsQA.cxx+g");
    gROOT->LoadMacro("AliAnalysisTaskCaloCellsQAPt.h+g");
    gROOT->LoadMacro("AddMyTask.C");

    AliAnalysisTaskSE * myTask = AddMyTask();

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
}

