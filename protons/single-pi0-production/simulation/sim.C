void sim(Int_t nev = 10, Int_t drain = 1)
{


	gSystem->AddIncludePath("-I$ALICE_ROOT/include -I$ALICE_PHYSICS/include -I$ALICE_ROOT/EVGEN");


	gSystem->Load("liblhapdf");
	gSystem->Load("libqpythia");
	gSystem->Load("libAliPythia6");
	gSystem->Load("libpythia6_4_21");
	gSystem->Load("libEGPythia6");
	gSystem->Load("libgeant321");



	AliSimulation simulator;

	if (gSystem->Getenv("CONFIG_SEED"))
	{
		seed = atoi(gSystem->Getenv("CONFIG_SEED"));
		seed = 100 * seed + 10 * seed + seed;
		simulator.SetSeed(seed);
	}


	//  simulator.SetWriteRawData("ALL","raw.root",kTRUE);
	simulator.SetMakeSDigits("PHOS ITS TPC");
	simulator.SetMakeDigits("PHOS ITS TPC");
	simulator.SetMakeDigitsFromHits("ITS TPC");

	simulator.SetRunQA(":");

	simulator.SetRunNumber(257733);

	simulator.SetDefaultStorage("alien://Folder=/alice/data/2016/OCDB");
	AliCDBManager* man = AliCDBManager::Instance();

	simulator.SetSpecificStorage("TPC/Calib/AltroConfig",    "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
	simulator.SetSpecificStorage("TPC/Calib/Correction",     "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
	simulator.SetSpecificStorage("TPC/Align/Data",           "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
	simulator.SetSpecificStorage("TPC/Calib/TimeDrift",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
	simulator.SetSpecificStorage("TPC/Calib/RecoParam",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");


	simulator.UseVertexFromCDB();
	simulator.UseMagFieldFromGRP();

	simulator.Run(nev);
	WriteXsection();
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
