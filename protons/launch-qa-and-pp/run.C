#include "algorithm"
void run(const char * runmode = "local", const char * pluginmode = "test", Bool_t isMC = kFALSE, Bool_t useJDL = kTRUE)
{
    SetupEnvironment();
    TString qa_dir = "";
    gROOT->LoadMacro("../../qa/qa-task/getRunsBadCells.C");

    TString pp_dir = "";

    TString period = "LHC16l-muon-calo-pass1";
    Bool_t use_tender = kTRUE;
    Int_t * excells;
    Int_t * good_runs;
    Int_t nexc;
    Int_t nruns;
    getRunsBadCells(period, good_runs, nruns, excells, nexc);


    gROOT->LoadMacro("CreatePlugin.C");
    AliAnalysisGrid * alienHandler = CreatePlugin(pluginmode, good_runs, nruns, period, "-2gev-test", qa_dir, pp_dir, useJDL);

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

    Bool_t enablePileupCuts = kFALSE;
    AddTaskPhysicsSelection (isMC, enablePileupCuts);  //false for data, true for MC

    //gROOT->LoadMacro(qa_dir + "AnalysisTaskCellsQA.cxx+g");
    gROOT->LoadMacro(qa_dir + "AliAnalysisTaskCaloCellsQAPt.h+g");
    gROOT->LoadMacro(qa_dir + "AddTaskCaloCellsQAPt.C");


    gROOT->LoadMacro(pp_dir + "PhotonSelection.cxx+");
    gROOT->LoadMacro(pp_dir + "TestPhotonSelection.cxx+");
    gROOT->LoadMacro(pp_dir + "PhysPhotonSelection.cxx+");
    gROOT->LoadMacro(pp_dir + "PhotonTimecutSelection.cxx+");
    gROOT->LoadMacro(pp_dir + "MixingSample.h+");
    gROOT->LoadMacro(pp_dir + "AliAnalysisTaskPP.cxx+");
    gROOT->LoadMacro(pp_dir + "AddAnalysisTaskPP.C");

    TString files = "";

    if (use_tender)
    {
        gROOT->LoadMacro("$ALICE_PHYSICS/PWGGA/PHOSTasks/PHOS_PbPb/AddAODPHOSTender.C");
        AliPHOSTenderTask * tenderPHOS = AddAODPHOSTender("PHOSTenderTask", "PHOStender") ;
        // AliPHOSTenderSupply * PHOSSupply = tenderPHOS->GetPHOSTenderSupply();
        // PHOSSupply->ForceUsingBadMap("BadMap_LHC16k.root");

        files += AddTaskCaloCellsQAPt(excells, nexc);
        files += AddAnalysisTaskPP(AliVEvent::kINT7, period + "## muon-calo-pass1, testing physics selection (pileup cuts) ## tender", "Tender", "", excells, nexc);
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

