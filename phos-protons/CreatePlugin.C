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


	// LHC16g
	Int_t RunNumbers[] = {     254128, 254147, 254148, 254149, 254174, 254175, 254178, 254193, 254196, 254199, 254204,
	                           254205, 254214, 254223, 254241, 254270, 254303, 254304, 254330, 254331, 254332
	                     };

	// LHC16h
	// Int_t RunNumbers[] =
	// {
	// 	254378, 254381, 254394, 254395, 254396, 254419, 254378, 254381, 254394, 254395, 254396,
	// 	254419, 254422, 254476, 254479, 254604, 254606, 254607, 254608, 254621, 254629, 254630,
	// 	254632, 254640, 254644, 254646, 254648, 254649, 254653, 254654, 254983, 254984, 255008,
	// 	255009, 255010,
	// 	// 255042, 255068, 255071, 255073, 255074, 255075, 255076,  // these are runs with low statistics, excluded
	// 	255079, 255082,
	// 	255085, 255086, 255091, 255111, 255154, 255159, 255162, 255167, 255171, 255173, 255176,
	// 	255177, 255180, 255182, 255240, 255242, 255247, 255248, 255249, 255251, 255252, 255253,
	// 	255255, 255256, 255275, 255276, 255278, 255280, 255283, 255350, 255351, 255352, 255398,
	// 	255402, 255407, 255440, 255442, 255447, 255463, 255465, 255466, 255467

	// };

	// LHC16i
	Int_t RunNumbers[] =
	{
		// There are 21 reconstructed runs. More precise: "good" runs 16
		255616, 255615, 255614, 255592, 255591, 255582, 255577, 255543, 255542, 255540, 
		255538, 255537, 255535, 255534, 255533, 255515,
		// 4 bad runs (all due to FMD)
		255618, 255617, 255583, 255539,
		// And one small run with duration < 10 min.
		255541	
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
