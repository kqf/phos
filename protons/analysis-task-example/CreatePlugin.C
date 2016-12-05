AliAnalysisGrid * CreatePlugin(TString pluginmode = "test", Bool_t mergeJDL = kTRUE, Int_t * runs, Int_t nruns, TString period)
{

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);

	plugin->SetMergeViaJDL(mergeJDL); 

	plugin->SetOutputToRunNo(kTRUE); 
	
	plugin->SetRunMode(pluginmode);

	plugin->SetAPIVersion("V1.1x");
	plugin->SetAliPhysicsVersion("vAN-20161203-1");


	plugin->SetExecutableCommand("aliroot");
	plugin->SetExecutableArgs("-b -q -x");

	plugin->SetCheckCopy(kFALSE);

	plugin->SetGridDataDir("/alice/data/2016/" + period);
	plugin->SetDataPattern("/muon_calo_pass1/*.*/AliAOD.root");
	// plugin->SetDataPattern("/muon_calo_pass1/*.*/AliESDs.root");
	plugin->SetRunPrefix("000");

	cout << "We are trying to analyse " << nruns << " runs" << endl;

    for (Int_t i = 0; i < nruns; ++i)
		plugin->AddRunNumber(runs[i]);

	plugin->SetDefaultOutputs(kFALSE);
	plugin->SetOutputFiles("AnalysisResults.root");

	plugin->SetGridWorkingDir("phos-protons-example");
	plugin->SetGridOutputDir(period);
	// plugin->SetDefaultOutputs();


	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	plugin->SetAnalysisSource("AliAnalysisTaskPi0v4.cxx");
	plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so AliAnalysisTaskPi0v4.cxx AliAnalysisTaskPi0v4.h");

	plugin->SetAnalysisMacro("TaskProtonsExample.C");
	plugin->SetSplitMaxInputFileNumber(100);
	plugin->SetExecutable("TaskProtonsExample.sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName("TaskProtonsExample.jdl");
	plugin->SetPrice(1);
	plugin->SetSplitMode("se");


	plugin->SetProofCluster ( "alice-caf.cern.ch" );
	plugin->SetProofDataSet ( "/alice/data/LHC10h_000138150_p2" );
	plugin->SetProofReset ( 0 );
	plugin->SetNproofWorkers ( 0 );


	plugin->SetAliRootMode ( "default" );
	plugin->SetClearPackages ( kFALSE );
	plugin->SetFileForTestMode ( "files.txt" );
	plugin->SetProofConnectGrid ( kFALSE );
	plugin->SetDropToShell(kFALSE);
	if (!plugin)
		cout << "Warning \n";
	return plugin;
}
