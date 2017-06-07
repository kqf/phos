void sim(Int_t nev = 10000)
{
	AliSimulation simulator;

	// simulator.SetMakeSDigits("PHOS");
	// simulator.SetMakeDigits("PHOS");

	simulator.SetMakeSDigits("PHOS ITS TPC");
	simulator.SetMakeDigits("PHOS ITS TPC");
	simulator.SetMakeDigitsFromHits("ITS TPC");


	simulator.SetDefaultStorage("alien://Folder=/alice/data/2016/OCDB");
	// Vertex and magfield

	simulator.UseVertexFromCDB();
	simulator.UseMagFieldFromGRP();

	// PHOS simulation settings
	AliPHOSSimParam *simParam = AliPHOSSimParam::GetInstance();
	simParam->SetCellNonLinearity(kFALSE);//switch off cell non-linearity

	simulator.SetRunQA(":");
	simulator.SetRunNumber(257733);


	if (gSystem->Getenv("CONFIG_SEED"))
	{
		seed = atoi(gSystem->Getenv("CONFIG_SEED"));
		seed = 100 * seed + 10 * seed + seed;
		simulator.SetSeed(seed);
	}	


	printf("Before simulator.Run(nev);\n");
	simulator.Run(nev);
	printf("After simulator.Run(nev);\n");
}