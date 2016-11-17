#include <TRandom.h>
#include <TSystem.h>
#include <TVirtualMC.h>

void fastGenEMCocktail_pp(Int_t nev = 1000, char * filename = "galice.root")
{
	SetupEnvironment();
	//===============
	static Int_t mesonPDG = 111; // PDG code of a neutral meson to generate

	Double_t yMin = -0.30;
	Double_t yMax =  0.30;

	Double_t phiMin = 240;
	Double_t phiMax = 340;

	//===============

	//seed
	if (gSystem->Getenv("CONFIG_SEED"))
		seed = atoi(gSystem->Getenv("CONFIG_SEED"));
	gRandom->SetSeed(1);
	cout << "seed = " << gRandom->GetSeed() << endl;


	// Runloader
	AliRunLoader * runloader = AliRunLoader::Open("galice.root", "FASTRUN", "recreate");
	runloader->SetCompressionLevel(2);
	runloader->SetNumberOfEventsPerFile(nev);
	runloader->LoadKinematics("RECREATE");
	runloader->MakeTree("E");
	gAlice->SetRunLoader(runloader);

	// Create stack
	runloader->MakeStack();
	AliStack * stack = runloader->Stack();

	// Header
	AliHeader * header = runloader->GetHeader();

	// Create and Initialize Decayer
	TVirtualMCDecayer * decayer = new AliDecayerPythia();
	decayer->SetForceDecay(kAll);
	decayer->Init();


	// TODO: rewrite me
	TString mesonParamFile = "pi0_Tsallis_pp_7Tev.root";
	TFile * fpp = TFile::Open(mesonParamFile);
	if (!fpp) Fatal("", Form("Cannot open file %s", mesonParamFile));
	TF1  * ptSpectrum = (TF1 *)fpp->Get("Tsalis");
	Info("", Form("\n\tGenerator %s is initialized\n", ptSpectrum->GetTitle()));

	gROOT->LoadMacro("AliGenPHOSMesons.h++") ;
	AliGenPHOSMesons * myGener = new AliGenPHOSMesons() ;


	AliGenParam * genMeson = new AliGenParam(20, AliGenPHOSlib::kPion,
	        myGener->GetPt(AliGenPHOSlib::kPion, ""),
	        myGener->GetY (AliGenPHOSlib::kPi0Flat, ""),
	        myGener->GetV2 (AliGenPHOSlib::kPi0Flat, ""),
	        myGener->GetIp(AliGenPHOSlib::kPion, ""));


	genMeson->SetPhiRange(phiMin, phiMax);
	genMeson->SetYRange  (yMin, yMax) ;
	genMeson->SetPtRange (0.5, 100.) ;
	genMeson->SetOrigin  (0, 0, 0);
	genMeson->SetSigma   (0., 0., 0.);
	genMeson->SetDecayer(decayer);

	AliGenCocktail * cocktail_generator = new AliGenCocktail();
	cocktail_generator->AddGenerator(genMeson, "Tsalis", 1) ;
	cocktail_generator->SetOrigin(0., 0., 0.);
	cocktail_generator->SetSigma(0., 0., 0.);
	cocktail_generator->Init();
	cocktail_generator->SetStack(stack);

	for (Int_t iev = 0; iev < nev; iev++)
	{
		cout << "Event number: " <<  iev << endl;

		// Initialize event
		header->Reset(0, iev);
		runloader->SetEventNumber(iev);
		stack->Reset();
		runloader->MakeTree("K");

		// Generate event
		cocktail_generator->Generate();

		// Finish event
		header->SetNprimary(stack->GetNprimary());
		header->SetNtrack(stack->GetNtrack());

		// I/O
		stack->FinishEvent();
		header->SetStack(stack);
		runloader->TreeE()->Fill();
		runloader->WriteKinematics("OVERWRITE");
	} //event loop

	//Termination
	cocktail_generator->FinishRun();
	//Write file
	runloader->WriteHeader("OVERWRITE");
	cocktail_generator->Write();
	runloader->Write();
}

void SetupEnvironment()
{
	gSystem->Load("libTree.so");
	gSystem->Load("libGeom.so");
	gSystem->Load("libVMC.so");
	gSystem->Load("libPhysics.so");

	//load analysis framework
	gSystem->Load("libANALYSIS");
	gSystem->Load("libANALYSISalice");

	//add include path
	gSystem->AddIncludePath("-I$ALICE_ROOT/include");
	gSystem->AddIncludePath("-I$ALICE_ROOT/PHOS");

	// load libraries
	gSystem->AddIncludePath("-I$ALICE_ROOT/include -I$ALICE_ROOT/EVGEN -I$ALICE_ROOT/STEER/STEER");

	gSystem->Load("liblhapdf.so");      // Parton density functions
	gSystem->Load("libqpythia.so");
	gSystem->Load("libpythia6.so");     // Pythia
	gSystem->Load("libEG.so");
	gSystem->Load("libEGPythia6.so");
	gSystem->Load("libqpythia.so");
	gSystem->Load("libAliPythia6.so");  // ALICE specific implementations

	// Lambda functions will not help here
	// TString o = TString(gSystem->GetMakeSharedLib());
	// o.ReplaceAll(" -c ", " -std=c++11 -c ");
}





void ProcessEnvironmentVars()
{
	// Colliding system
	if (gSystem->Getenv("CONFIG_BEAMS"))
		beams = gSystem->Getenv("CONFIG_BEAMS");

	// PDG code of neutral meson
	if (gSystem->Getenv("CONFIG_MESON_PDG"))
		mesonPDG = atoi(gSystem->Getenv("CONFIG_MESON_PDG"));

	// Random Number seed
	if (gSystem->Getenv("CONFIG_SEED"))
		sseed = atoi(gSystem->Getenv("CONFIG_SEED"));


}
