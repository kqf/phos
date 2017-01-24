void sim(Int_t nev = 1, Int_t drain = 1)
{


	gSystem->AddIncludePath("-I$ALICE_ROOT/include -I$ALICE_PHYSICS/include -I$ALICE_ROOT/EVGEN");
	gSystem->Load("liblhapdf");
	gSystem->Load("libqpythia");
	gSystem->Load("libAliPythia6");
	gSystem->Load("libpythia6_4_21");
	gSystem->Load("libEGPythia6");
	gSystem->Load("libgeant321");

	// gROOT->LoadMacro("AliAnalysisTaskPi0.h++") ;

	AliSimulation simulator;
	// simulator.SetWriteRawData("ALL","raw.root",kTRUE);
	// simulator.SetMakeSDigits("TOF PHOS HMPID EMCAL MUON FMD ZDC PMD T0 VZERO");
	// simulator.SetMakeDigits("ITS TPC TOF PHOS HMPID EMCAL MUON FMD ZDC PMD T0 VZERO");
	// simulator.SetMakeDigitsFromHits("ITS TPC");
	// simulator.SetMakeSDigits("PHOS");
	// simulator.SetMakeDigits("PHOS");
	// simulator.SetWriteRawData("ALL","raw.root",kTRUE);
	simulator.SetMakeSDigits("PHOS ITS TPC");
	simulator.SetMakeDigits("PHOS ITS TPC");


	simulator.SetRunQA(":");

	simulator.SetRunNumber(130795);
	simulator.SetDefaultStorage("local://OCDBdrain/alice/data/2010/OCDB");
	AliCDBManager* man = AliCDBManager::Instance();



	// Vertex and Mag.field from OCDB
	simulator.UseVertexFromCDB();
	simulator.UseMagFieldFromGRP();

	//
	// The rest
	//

	simulator.Run(nev);
	WriteXsection();

	// timerSim.Print();

}


WriteXsection()
{
	TPythia6 *pythia = TPythia6::Instance();
	pythia->Pystat(1);
	Double_t xsection = pythia->GetPARI(1);
	UInt_t    ntrials  = pythia->GetMSTI(5);

	TFile *file = new TFile("pyxsec.root", "recreate");
	TTree   *tree   = new TTree("Xsection", "Pythia cross section");
	TBranch *branch = tree->Branch("xsection", &xsection, "X/D");
	TBranch *branch = tree->Branch("ntrials" , &ntrials , "X/i");
	tree->Fill();



	tree->Write();
	file->Close();

	cout << "Pythia cross section: " << xsection
	     << ", number of trials: " << ntrials << endl;
}
