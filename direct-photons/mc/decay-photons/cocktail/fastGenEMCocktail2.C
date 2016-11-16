#include <TRandom.h>
#include <TSystem.h>
#include <TVirtualMC.h>

void ProcessEnvironmentVars();
void fastGenEMCocktail2(Int_t nev = 1000, char * filename = "galice.root")
{

	static Int_t mesonPDG =   111; // PDG code of a neutral meson to generate

	//===============

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

	//===============

	Double_t yMin = -0.30;
	Double_t yMax =  0.30;

	Double_t phiMin = 240;
	Double_t phiMax = 340;

	// load libraries
	gSystem->AddIncludePath("-I$ALICE_ROOT/include -I$ALICE_ROOT/EVGEN -I$ALICE_ROOT/STEER/STEER");

	gSystem->Load("liblhapdf.so");      // Parton density functions
	gSystem->Load("libqpythia.so");
	gSystem->Load("libpythia6.so");     // Pythia
	gSystem->Load("libEG.so");
	gSystem->Load("libEGPythia6.so");
	gSystem->Load("libqpythia.so");
	gSystem->Load("libAliPythia6.so");  // ALICE specific implementations

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





	gROOT->LoadMacro("AliGenPHOSlibPlus.h++") ;


	// AliGenerator *gener  = new AliGenerator();

	//=======================================================================
	// Set External decayer
	TVirtualMCDecayer * decayer = new AliDecayerPythia();



	//    TString mesonParamFile = "_2.76TeV_SpectraParam.root";
	//TString mesonParamFile = "PbPb_2.76TeV_Tsallis_cen0.root";
	TString mesonParamFile = "pi0_Tsallis_pp_7Tev.root";
	// mesonParamFile.Prepend(beams);
	/*
	   TString ptSpectrumName = "Tsallis";
	   if (mesonPDG == 111)
	   ptSpectrumName = "pi0Spectrum";
	   else if (mesonPDG == 221)
	   ptSpectrumName = "etaSpectrum";
	   else if (mesonPDG == 223)
	   ptSpectrumName = "omegaSpectrum";
	   else if (mesonPDG == 331)
	   ptSpectrumName = "etaprimeSpectrum";
	   else
	   Fatal("",Form("Unknown meson PDF code to generate: %d",mesonPDG));
	 */
	TFile * fpp = TFile::Open(mesonParamFile);
	if (!fpp)
		Fatal("", Form("Cannot open file %s", mesonParamFile));

	//TF1*   ptSpectrum = (TF1*)fpp->Get("TsallisPi0");
	TF1  * ptSpectrum = (TF1 *)fpp->Get("Tsalis");
	Info("", Form("\n\tGenerator %s is initialized\n", ptSpectrum->GetTitle()));

	AliGenPHOSlibPlus * myGener = new AliGenPHOSlibPlus(mesonPDG, ptSpectrum) ;




	AliGenParam * genMeson = new AliGenParam(20, AliGenPHOSlib::kPion,
			myGener->GetPt(AliGenPHOSlib::kPion, ""),
			myGener->GetY (AliGenPHOSlib::kPi0Flat, ""),
			myGener->GetV2 (AliGenPHOSlib::kPi0Flat, ""),
			myGener->GetIp(1, ""));



	genMeson->SetPhiRange(phiMin, phiMax);
	genMeson->SetYRange  (yMin, yMax) ;
	genMeson->SetPtRange (0.5, 100.) ;
	genMeson->SetOrigin  (0, 0, 0);
	genMeson->SetSigma   (0., 0., 0.);



	AliGenCocktail * gener = new AliGenCocktail();


	// gener->AddGenerator(genMeson,ptSpectrumName,1) ;

	//gener->SetDecayMode(kGammaEM);    // select cocktail:
	// kElectronEM   => single electron
	// kDiElectronEM => electron-positron
	// kGammaEM      => single photon
	// kAll => All resonances
	// gener->SetDecayer(decayer);
	// gener->SetWeightingMode(kNonAnalog); // select weighting:
	// kNonAnalog => weight ~ dN/dp_T
	// kAnalog    => weight ~ 1


	//gener->CreateCocktail();





	// gener->Init();

	genMeson->SetDecayer(decayer);

	decayer->SetForceDecay(kAll);
	decayer->Init();

	genMeson->Init();
	//  gener->SetStack(stack);
	genMeson->SetStack(stack);


	//
	//                        Event Loop
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
		genMeson->Generate();
		// Analysis
		Int_t npart = stack->GetNprimary();
		// printf("Analyse %d Particles\n", npart);
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
	genMeson->FinishRun();
	//Write file
	rl->WriteHeader("OVERWRITE");
	genMeson->Write();
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
