AliAnalysisGrid * CreatePlugin(const char * pluginmode = "test")
{

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);

	plugin->SetRunMode(pluginmode);

	plugin->SetAPIVersion("V1.1x");
	// plugin->SetAliROOTVersion("v5-05-Rev-18");
	plugin->SetAliPhysicsVersion("v5-08-08-01-1");
	// plugin->SetAliPhysicsVersion("vAN-20150818");


	plugin->SetExecutableCommand("aliroot");
	plugin->SetExecutableArgs("-b -q -x");

	plugin->SetCheckCopy(kFALSE);

	// plugin->SetGridDataDir("/alice/data/2010/LHC10e/");
	plugin->SetGridDataDir("/alice/data/2016/LHC16g/");
	plugin->SetDataPattern("/muon_calo_pass1/*.*/AliAOD.root");
	// plugin->SetDataPattern("/muon_calo_pass1/*.*/AliESDs.root");
	plugin->SetRunPrefix("000");
	// plugin->AddRunNumber(254178);

	// plugin->SetGridDataDir("/alice/sim/2013/LHC13d15/");
	// plugin->SetDataPattern("*ESDs.root");
	// plugin->SetRunPrefix("");


	Int_t RunNumbers[] = {     254128, 254147, 254148, 254149, 254174, 254175, 254178, 254193, 254196, 254199, 254204,
	                           254205, 254214, 254223, 254241, 254270, 254303, 254304, 254330, 254331, 254332
	                     };

	Int_t nRuns = sizeof(RunNumbers) / sizeof(Int_t);
	cout << "We are trying to analyse " << nRuns << " runs" << endl;

	for (Int_t i = 0; i < nRuns; ++i)
		plugin->AddRunNumber(RunNumbers[i]);

	// plugin->AddRunNumber(RunNumbers[0]);
	// plugin->AddRunNumber(RunNumbers[1]);


	plugin->SetDefaultOutputs(kFALSE);
	plugin->SetOutputFiles("AnalysisResults.root");

	plugin->SetGridWorkingDir("phos-protons");
	plugin->SetGridOutputDir("output");
	// plugin->SetDefaultOutputs();
	// Now this should be added in your AddTaskMacro.C

	// plugin->SetAnalysisSource("ChargedTrack.h MyTaskHelper.cxx AliAnalysisTaskSimplePt.cxx");
	// plugin->SetAdditionalLibs("ChargedTrack.h MyTaskHelper.h MyTaskHelper.cxx AliAnalysisTaskSimplePt.h AliAnalysisTaskSimplePt.cxx");

	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	plugin->SetAnalysisSource("PhotonSelection.cxx TestPhotonSelection.cxx PhysPhotonSelection.cxx AliAnalysisTaskPrompt.cxx");
	plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so PhotonSelection.cxx PhotonSelection.h TestPhotonSelection.cxx TestPhotonSelection.h PhysPhotonSelection.cxx PhysPhotonSelection.h AliAnalysisTaskPrompt.cxx AliAnalysisTaskPrompt.h");

	plugin->SetAnalysisMacro("TaskPrompt.C");
	plugin->SetSplitMaxInputFileNumber(100);
	plugin->SetExecutable("TaskPrompt.sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName("TaskPrompt.jdl");
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
