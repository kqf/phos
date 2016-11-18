#include <TRandom.h>
#include <TSystem.h>
#include <TVirtualMC.h>

void fastGenEMCocktail_pp(Int_t nev = 1000, char * filename = "galice.root")
{
	SetupEnvironment();
	//===============
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
	gROOT->LoadMacro("AliGenPHOSMesons.h++") ;
	AliGenPHOSMesons * myGener = new AliGenPHOSMesons() ;

	AliGenParam * genMesons[] = {    new AliGenParam(20, myGener, AliGenPHOSlib::kPion, "")
									,new AliGenParam(20, myGener, AliGenPHOSlib::kEta, "") 
									,new AliGenParam(20, myGener, AliGenPHOSlib::kOmega, "") 
								};

	Int_t nComponents = sizeof(genMesons)/sizeof(AliGenParam *);
	for(Int_t i = 0; i < nComponents; ++i)
	{
		genMesons[i]->SetPhiRange(phiMin, phiMax);
		genMesons[i]->SetYRange  (yMin, yMax) ;
		genMesons[i]->SetPtRange (0.5, 100.) ;
		genMesons[i]->SetOrigin  (0, 0, 0);
		genMesons[i]->SetSigma   (0., 0., 0.);
		genMesons[i]->SetDecayer(decayer);
	}

	AliGenCocktail * cocktail_generator = new AliGenCocktail();
	for(Int_t i = 0; i < nComponents; ++i) 
		cocktail_generator->AddGenerator(genMesons[i], "Tsalis", 1) ;
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

	// Random Number seed
	if (gSystem->Getenv("CONFIG_SEED"))
		sseed = atoi(gSystem->Getenv("CONFIG_SEED"));
}
