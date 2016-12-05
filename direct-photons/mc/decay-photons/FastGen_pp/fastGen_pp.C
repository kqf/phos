#include <TRandom.h>
#include <TSystem.h>
#include <TVirtualMC.h>

//void ProcessEnvironmentVars();
void fastGen_pp(Int_t nev = 50, char * filename = "galice.root")
{
	// load libraries
	gSystem->AddIncludePath("-I$ALICE_ROOT/include -I$ALICE_ROOT/EVGEN -I$ALICE_PHYSICS/include");


	gSystem->Load("liblhapdf");
	gSystem->Load("libpythia6");
	// gSystem->Load("libpythia6_4_28");
	// gSystem->Load("libqpythia");
	gSystem->Load("libEG");
	gSystem->Load("libEGPythia6");
	gSystem->Load("libAliPythia6");


	// gSystem->ListLibraries()->Print();

	//seed

	//static Int_t    sseed = 0; //Set 0 to use the current time
	//TDatime tt;
	//static Int_t seed    = tt.Get();



	gRandom->SetSeed(0);

	if (gSystem->Getenv("CONFIG_SEED"))
		seed = atoi(gSystem->Getenv("CONFIG_SEED"));

	cout << "seed=" << gRandom->GetSeed() << endl;


	// Runloader

	AliRunLoader * rl = AliRunLoader::Open("galice.root", "FASTRUN", "recreate");

	rl->SetCompressionLevel(2);
	rl->SetNumberOfEventsPerFile(nev);
	rl->LoadKinematics("RECREATE");
	rl->MakeTree("E");
	gAlice->SetRunLoader(rl);

	// Create stack
	rl->MakeStack();
	AliStack * stack      = rl->Stack();

	// Header
	AliHeader * header = rl->GetHeader();

	// Create and Initialize Generator





	// gROOT->LoadMacro("AliGenPHOSlibPlus.h++") ;


	// AliGenerator *gener  = new AliGenerator();

	//=======================================================================
	// Set External decayer

	// Set the trigger configuration
	AliSimulation::Instance()->SetTriggerConfig("p-p");
	cout << "Trigger configuration is set to  " << "kDefaultPPTrig" << endl;

	//
	// Set External decayer
	// AliDecayer *decayer = new AliDecayerPythia();
	AliDecayerPythia * decayer = new AliDecayerPythia();
	decayer->DecayLongLivedParticles();
	decayer->SetForceDecay(kAll);
	decayer->Init();
	//  vmc->SetExternalDecayer(decayer);

	// AliGenPythia * gener = new AliGenPythia(-1);
	// AliGenPythia * gener = new AliGenPythia(1);
	AliGenPythia * gener = new AliGenPythia(10000);
	gener->SetMomentumRange(0, 999999);
	gener->SetThetaRange(0., 180.);
	gener->SetYRange(-1, 1);
	gener->SetPtRange(0, 10000);
	gener->SetProcess(kPyMb);
	gener->SetEnergyCMS(7000.);
	gener->SetProjectile("p", 1, 1) ;
	gener->SetTarget("p", 1, 1) ;
	gGener = gener;

	gener->SetOrigin(0, 0, 0);    // vertex position
	gener->SetSigma(0, 0, 5.3);   // Sigma in (X,Y,Z) (cm) on IP position
	gener->SetCutVertexZ(1.);     // Truncate at 1 sigma
	gener->SetVertexSmear(kPerEvent);
	gener->SetTrackingFlag(0);
	gener->Init();
	gener->SetStack(stack);

	//
	//  Event Loop
	//

	Int_t iev;

	for (iev = 0; iev < nev; iev++)
	{

		printf("\n \n Event number %d \n \n", iev);

		// Initialize event
		header->Reset(0, iev);
		rl->SetEventNumber(iev);
		stack->Reset();
		rl->MakeTree("K");
		//  stack->ConnectTree();

		// Generate event
		gener->Generate();
		// Analysis
		Int_t npart = stack->GetNprimary();
		printf("Analyse %d Particles\n", npart);
		for (Int_t part = 0; part < npart; part++)
		{
			// printf("Analysing %d \n", part);
			TParticle * MPart = stack->Particle(part);
			Int_t mpart  = MPart->GetPdgCode();
			// printf("Particle %d\n", mpart);


		}

		// Finish event
		header->SetNprimary(stack->GetNprimary());
		header->SetNtrack(stack->GetNtrack());
		// I/O
		// +
		stack->FinishEvent();
		header->SetStack(stack);
		rl->TreeE()->Fill();
		rl->WriteKinematics("OVERWRITE");

	} //event loop

	//Termination
	//Generator
	gener->FinishRun();
	//Write file
	rl->WriteHeader("OVERWRITE");
	gener->Write();
	rl->Write();
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
