readKine()
{
	gROOT->LoadMacro("fastGenEMCocktail_pp.C");
	SetupEnvironment();

	gROOT->LoadMacro("ParticleKinematics.h+");

	// Read primary particles from Kinematics.root,
	// look for pi0 and and print them
	AliRunLoader * runloader = AliRunLoader::Open("galice.root");

	ParticleKinematics particles[] =
	{
		  ParticleKinematics(ParticleKinematics::kAny)
		, ParticleKinematics(ParticleKinematics::kPion)
		, ParticleKinematics(ParticleKinematics::kEta)
		, ParticleKinematics(ParticleKinematics::kOmega)
	};
	Int_t nspecies = sizeof(particles) / sizeof(ParticleKinematics);

	TH1F * counter = new TH1F("hCounter", "Event counter", 1, 0, 1);

	for (Int_t ievent = 0; ievent < runloader->GetNumberOfEvents(); ievent++)
	{
		counter->Fill(0.5);
		cout << "Processing event # " << ievent << endl;

		runloader->GetEvent(ievent);
		runloader->LoadKinematics();
		AliStack * stack = runloader->Stack();

		for (Int_t iPrim = 0; iPrim < stack->GetNprimary(); iPrim++)
		{
			TParticle * particle = stack->Particle(iPrim);

			for (int i = 0; i < nspecies; ++i)
				particles[i].Fill(stack, particle);
		}
	}

	TFile ff("generated.root", "recreate");
	counter->Write();
	for (int i = 0; i < nspecies; ++i) 
		particles[i].Write();

	ff.Close();
}