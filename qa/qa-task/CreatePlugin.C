AliAnalysisGrid * CreatePlugin(const char * pluginmode = "test",Int_t * runs, Int_t nruns, TString period, TString comment)
{
	if (period.Length() < 6) 
		cerr << "Error: Wrong run period (too short)" << period << endl;

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);
	
	plugin->SetMergeViaJDL(); 
	plugin->SetOutputToRunNo(kTRUE); 


	plugin->SetRunMode(pluginmode);

	plugin->SetAPIVersion("V1.1x");
	plugin->SetAliPhysicsVersion("vAN-20160717-1");


	plugin->SetExecutableCommand("aliroot");
	plugin->SetExecutableArgs("-b -q -x");

	plugin->SetCheckCopy(kFALSE);

	TString dir(period, 6); // fancy slicing
	plugin->SetGridDataDir("/alice/data/2016/" + dir);
	cout << "/alice/data/2016/" + dir << endl;
	plugin->SetDataPattern("/muon_calo_pass1/*.*/AliAOD.root");
	// plugin->SetDataPattern("/muon_calo_pass1/*.*/AliESDs.root");
	plugin->SetRunPrefix("000");



	cout << "We are trying to analyse " << nruns << " runs" << endl;

	for (Int_t i = 0; i < nruns; ++i)
		plugin->AddRunNumber(runs[i]);

	plugin->SetDefaultOutputs(kFALSE);
	plugin->SetOutputFiles("CaloCellsQA2.root");
	// plugin->SetOutputFiles("CaloCellsQA2.root TriggerQA.root");
	// plugin->SetOutputFiles("TriggerQA.root");

	period.ToLower();
	plugin->SetGridWorkingDir("phosqa-" + period + "-muon-calo-pass1" + comment);
	// plugin->SetGridWorkingDir("phosqa-16h-muon-calo-pass1-good-tender");
	plugin->SetGridOutputDir("output");
	// plugin->SetDefaultOutputs();
	// Now this should be added in your AddTaskMacro.C


	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	// plugin->SetAnalysisSource("AliAnalysisTaskPi0QA.cxx");
	// plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so");// AliAnalysisTaskPi0QA.cxx AliAnalysisTaskPi0QA.h");

	plugin->SetAnalysisSource("AliAnalysisTaskCaloCellsQAPt.h");
	plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so AliAnalysisTaskCaloCellsQAPt.h");

	plugin->SetAnalysisMacro(TString("TaskQA") + period + ".C");
	plugin->SetSplitMaxInputFileNumber(100);
	plugin->SetExecutable(TString("TaskQA") + period + ".sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName(TString("TaskQA") + period + ".jdl");
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
