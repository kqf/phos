#include "algorithm"
void run(const char * runmode = "local", const char * pluginmode = "test", bool isMC = false)
{
    SetupEnvironment();

    TString period = "LHC16o";
    Int_t * excells;
    Int_t * good_runs;
    Int_t nexc;
    Int_t nruns;
    gROOT->LoadMacro("getRunsBadCells.C");
    getRunsBadCells(period, good_runs, nruns, excells, nexc);


    gROOT->LoadMacro("CreatePlugin.C");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, good_runs, nruns, period, "-2gev-test");

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
        mchandler->SetReadTR ( kFALSE ); // Don't read track references
        mgr->SetMCtruthEventHandler ( mchandler );
    }

    // Connect plug-in to the analysis manager
    mgr->SetGridHandler(alienHandler);

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection ( isMC );  //false for data, true for MC

    if (period.Contains("tender"))
    {
        gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
        AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
        AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
        PHOSSupply->ForceUsingBadMap("BadMap_LHC16g.root");
        // PHOSSupply->ForceUsingCalibration(0);
    }
    // gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_TriggerQA/macros/AddTaskPHOSTriggerQA.C");
    // AliAnalysisTaskPHOSTriggerQA * triggertask = AddTaskPHOSTriggerQA("TriggerQA.root", "TriggerQA");
    // triggertask->SelectCollisionCandidates(AliVEvent::kINT7);


    // gROOT->LoadMacro("AddTasksTriggerQA.C");
    // AddTasksTriggerQA();

    gROOT->LoadMacro("AliAnalysisTaskPi0QA.cxx+");
    gROOT->LoadMacro("AnalysisTaskCellsQA.cxx+g");
    gROOT->LoadMacro("AliAnalysisTaskCaloCellsQAPt.h+g");
    gROOT->LoadMacro("AddMyTask.C");

    AliAnalysisTaskSE * myTask = AddMyTask(excells, nexc);

    if ( !mgr->InitAnalysis( ) ) return;
    mgr->PrintStatus();


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

