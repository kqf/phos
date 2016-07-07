void RunPoD(
  TString dataset = "Find;"
					"BasePath=/alice/data/2016/LHC16g/000254304/muon_calo_pass1/AOD/*/;"
					"FileName=AliAOD.root;"
					// "FileName=root_archive.zip;"
					// "Anchor=AliAOD.root;"
					"Tree=/aodTree;"
					"Mode=remote;",  // <-- much faster dataset creation
  Int_t numEvents = 999999999,
  Int_t firstEvent = 0
)
{

	// Not needed on the VAF
	//gEnv->SetValue("XSec.GSI.DelegProxy","2");

	TString extraLibs = "ANALYSIS:ANALYSISalice"; // extraLibs = "ANALYSIS:OADB:ANALYSISalice:CORRFW:OADB:PWGmuon";

	TList * list = new TList();
	list->Add(new TNamed("ALIROOT_EXTRA_LIBS", extraLibs.Data()));
	list->Add(new TNamed("ALIROOT_ENABLE_ALIEN", "1"));  // important: creates token on every PROOF worker

	// Not needed on the VAF
	//TProof::Mgr("alice-caf.cern.ch")->SetROOTVersion("VO_ALICE@ROOT::v5-34-08");

	// Note the difference between CAF and VAF
	//TProof::Open("alice-caf.cern.ch");
	TProof::Open("pod://");

	// Check the dataset before running the analysis!
	gProof->ShowDataSet( dataset.Data() );
	//return;  // <-- uncomment this to test search before running the analysis!

	// Not needed on the VAF
	//gProof->EnablePackage("VO_ALICE@AliRoot::v5-04-81-AN", list);

	// A single AliRoot package for *all* AliRoot versions: new on VAF
	TString aliceVafPar = "/afs/cern.ch/alice/offline/vaf/AliceVaf.par";
	gProof->UploadPackage(aliceVafPar.Data());
	gProof->EnablePackage(aliceVafPar.Data(), list);  // this "list" is the same as always

	AliAnalysisManager * mgr  = new AliAnalysisManager("Analysis Train");
	AliAODInputHandler * aodH = new AliAODInputHandler();
    AliESDInputHandler * esdH = new AliESDInputHandler();

    bool isMC = false;
    esdH->SetReadFriends( isMC );
    // mgr->SetInputEventHandler( esdH );
    mgr->SetInputEventHandler( aodH );
    esdH->SetNeedField();

    gROOT->LoadMacro ("$ALICE_PHYSICS/OADB/macros/AddTaskPhysicsSelection.C");
    AddTaskPhysicsSelection ( isMC );  //false for data, true for MC

	gProof->Load("PhotonSelection.cxx++");
    gProof->Load("TestPhotonSelection.cxx++");
    gProof->Load("PhysPhotonSelection.cxx++"); 
	gProof->Load("AliAnalysisTaskPrompt.cxx++");
	gSystem->SetMakeSharedLib(TString(gSystem->GetMakeSharedLib()).Insert(19, " -Wall ") );
	gROOT->LoadMacro("AddMyTask.C");


	AliAnalysisTaskSE * myTask = AddMyTask(AliVEvent::kINT7);



	if (!mgr->InitAnalysis()) return;
	
    mgr->SetSkipTerminate(kTRUE);
	mgr->StartAnalysis("proof", dataset, numEvents, firstEvent);

}
