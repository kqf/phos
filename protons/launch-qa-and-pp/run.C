#include "algorithm"
void run(const char * runmode = "local", const char * pluginmode = "test", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    gROOT->LoadMacro("../../qa/qa-task/getRunsBadCells.C");

    TString period = "LHC16l-muon-calo-pass1";
    Bool_t use_tender = kTRUE;
    Int_t * excells;
    Int_t * good_runs;
    Int_t nexc;
    Int_t nruns;
    getRunsBadCells(period, good_runs, nruns, excells, nexc);


    gROOT->LoadMacro("CreatePlugin.C");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, good_runs, nruns, period, "", useJDL);

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

    Bool_t enablePileupCuts = kTRUE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    //gROOT->LoadMacro("AnalysisTaskCellsQA.cxx+g");
    gROOT->LoadMacro("AliAnalysisTaskCaloCellsQAPt.h+g");
    gROOT->LoadMacro("AddTaskCaloCellsQAPt.C");
    gROOT->LoadMacro("AddAnalysisTaskPP.C");
    gROOT->LoadMacro("../../qa/qa-track-averages/AddAnalysisTaskTrackAverages.C");

    TString files = "";

    if (use_tender)
    {
        gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
        AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
        AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
        PHOSSupply->ForceUsingBadMap("BadMap_LHC16.root");

        // There is no need to download QA when we use don't use JDL
        if (useJDL)
            files += AddTaskCaloCellsQAPt(excells, nexc);

        files += AddAnalysisTaskPP(AliVEvent::kINT7, period + "## 12.5ns timecut, checking performance of the new map of bad channels ## tender", "Tender", "", excells, nexc);
        AddAnalysisTaskPP(AliVEvent::kINT7, period + "## 12.5ns timecut, checking performance of the new map of bad channels ## only tender", "OnlyTender", "", 0, 0);
        AddAnalysisTaskTrackAverages(good_runs, nruns);
    }


    if ( !mgr->InitAnalysis( ) ) return;
    mgr->PrintStatus();


    alienHandler->SetOutputFiles(files);
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

