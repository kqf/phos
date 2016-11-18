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
		  ParticleKinematics(ParticleKinematics::kPion)
		, ParticleKinematics(ParticleKinematics::kEta)
		, ParticleKinematics(ParticleKinematics::kOmega)
	};
	Int_t nspecies = sizeof(particles) / sizeof(ParticleKinematics);

	TH1F * totalGammas = new TH1F("hgenGamma", "Total amount of #gamma-s p_{T}; p_{t}, GeV/c; counts", 250, 0, 25);

	for (Int_t ievent = 0; ievent < runloader->GetNumberOfEvents(); ievent++)
	{
		cout << "Processing event # " << ievent << endl;

		runloader->GetEvent(ievent);
		runloader->LoadKinematics();
		AliStack * stack = runloader->Stack();

		for (Int_t iPrim = 0; iPrim < stack->GetNprimary(); iPrim++)
		{
			TParticle * particle = stack->Particle(iPrim);

			for (int i = 0; i < nspecies; ++i)
				particles[i].Fill(stack, particle);

			if(particle->GetPdgCode() == 22) 
				totalGammas->Fill(particle->Pt());
		}
	}

	TFile ff("generated.root", "recreate");
	totalGammas->Write();
	for (int i = 0; i < nspecies; ++i) 
		particles[i].Write();

	ff.Close();
}