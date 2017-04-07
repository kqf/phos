AliAnalysisGrid * CreatePlugin(const char * pluginmode = "test", Int_t * runs, Int_t nruns, TString period, TString comment, Bool_t useJDL, Bool_t isMC)
{
	if (period.Length() < 6)
		cerr << "Error: Wrong run period (too short)" << period << endl;

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);

	plugin->SetMergeViaJDL(useJDL);
	plugin->SetOutputToRunNo(kTRUE);


	plugin->SetRunMode(pluginmode);

	plugin->SetAPIVersion("V1.1x");
	plugin->SetAliPhysicsVersion("vAN-20170222-1");


	plugin->SetExecutableCommand("aliroot");
	plugin->SetExecutableArgs("-b -q -x");

	plugin->SetCheckCopy(kFALSE);

	// Extract period and reconstruction pass
	TString dir(period, isMC ? 9 : 6); // fancy slicing
	TString reconstruction(period);
	reconstruction.ReplaceAll(dir + (reconstruction.Contains(dir + "-") ? "-" : "") , "");
	reconstruction.ReplaceAll("-", "_");

	TString globaldir = isMC ? "/alice/sim/2016/" : "/alice/data/2016/";
	plugin->SetGridDataDir(globaldir + dir);
	cout << "/alice/data/2016/" + dir << endl;

	TString datasuffix = isMC ? "AOD/" : "/*.";
	plugin->SetDataPattern("/" + reconstruction + datasuffix + "*/AliAOD.root");
	cout << "Data pattern " << "/" + reconstruction + "/*.*/AliAOD.root" << endl;

	// plugin->SetDataPattern("/" + reconstruction + "/AOD/*/AliAOD.root");
	// plugin->SetDataPattern("/muon_calo_pass1/*.*/AliESDs.root");
	if(!isMC)
		plugin->SetRunPrefix("000");

	cout << "We are trying to analyse " << nruns << " runs" << endl;

	for (Int_t i = 0; i < nruns; ++i)
		plugin->AddRunNumber(runs[i]);

	plugin->SetDefaultOutputs(kFALSE);
	// plugin->SetOutputFiles("CaloCellsQA2.root TriggerQA.root");
	// plugin->SetOutputFiles("TriggerQA.root");

	period.ToLower();
	plugin->SetGridWorkingDir("pp-phos-" + period + comment);
	// plugin->SetGridWorkingDir("phos-16h-muon-calo-pass1-good-tender");
	plugin->SetGridOutputDir("output");
	// plugin->SetDefaultOutputs();
	// Now this should be added in your AddTaskMacro.C


	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	// plugin->SetAnalysisSource("AliAnalysisTaskPi0QA.cxx");
	// plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so");// AliAnalysisTaskPi0QA.cxx AliAnalysisTaskPi0QA.h");

	period.ReplaceAll('-', '_');

	// All files are set in the Add*Task.C macros
	// plugin->SetAnalysisSource();
	// plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so ");

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
