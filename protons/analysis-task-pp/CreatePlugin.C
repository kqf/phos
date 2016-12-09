AliAnalysisGrid * CreatePlugin(TString pluginmode = "test", Bool_t mergeJDL = kTRUE, Int_t * runs, Int_t nruns, TString period)
{

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);

    plugin->SetMergeViaJDL(mergeJDL); 
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

    for (Int_t i = 0; i < 1; ++i)
    // for (Int_t i = 0; i < nruns; ++i)
		plugin->AddRunNumber(runs[i]);

	plugin->SetDefaultOutputs(kFALSE);
	// plugin->SetOutputFiles("AnalysisResults.root");

	plugin->SetGridWorkingDir("phos-protons");
	plugin->SetGridOutputDir(period);
	// plugin->SetDefaultOutputs();


	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	plugin->SetAnalysisSource("PhotonSelection.cxx TestPhotonSelection.cxx PhysPhotonSelection.cxx PhotonTimecutSelection.h MixingSample.h AliAnalysisTaskPP.cxx");
	plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so PhotonSelection.cxx PhotonSelection.h TestPhotonSelection.cxx TestPhotonSelection.h PhysPhotonSelection.cxx PhysPhotonSelection.h PhotonTimecutSelection.h MixingSample.h AliAnalysisTaskPP.cxx AliAnalysisTaskPP.h");

	plugin->SetAnalysisMacro("TaskProtons.C");
	plugin->SetSplitMaxInputFileNumber(100);
	plugin->SetExecutable("TaskProtons.sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName("TaskProtons.jdl");
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
