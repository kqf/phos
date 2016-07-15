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

	// plugin->SetGridDataDir("/alice/data/2015/LHC15i");
	// plugin->SetGridDataDir("/alice/data/2016/LHC16g");
	// plugin->SetGridDataDir("/alice/data/2016/LHC16h");
	plugin->SetGridDataDir("/alice/data/2016/LHC16i");
	plugin->SetDataPattern("/muon_calo_pass1/*.*/AliAOD.root");
	plugin->SetRunPrefix("000");
	// plugin->AddRunNumber(236137);

	// plugin->SetGridDataDir("/alice/sim/2013/LHC13d15/");
	// plugin->SetDataPattern("*ESDs.root");
	// plugin->SetRunPrefix("");


	//236386,
	//236395,
	//236397,
	//236818,
	// 236822,

// LHC15i
// Int_t RunNumbers[] = {
	// 236137, 236138, 236150, 236151, 236153, 236158, 236161, 236163, 236204, 236222, 236227, 236234, 236238,
	// 236240, 236242, 236244, 236246, 236248, 236348, 236349, 236352, 236353, 236354, 236356, 236359, 236389,
	// 236393, 236441, 236443, 236444, 236556, 236558, 236562, 236563, 236564, 236565, 236813, 236814,
	// 236815, 236816, 236821, 236824, 236835, 236848, 236850, 236860, 236862, 236863, 236866};

	// LHC16g
	// Int_t RunNumbers[] = {     254128, 254147, 254148, 254149, 254174, 254175, 254178, 254193, 254196, 254199, 254204,
	// 254205, 254214, 254223, 254241, 254270, 254303, 254304, 254330, 254331, 254332
	// };

	// LHC16h
	// Int_t RunNumbers[] =
	// {
	// 254378, 254381, 254394, 254395, 254396, 254419, 254378, 254381, 254394, 254395, 254396,
	// 254419, 254422, 254476, 254479, 254604, 254606, 254607, 254608, 254621, 254629, 254630,
	// 254632, 254640, 254644, 254646, 254648, 254649, 254653, 254654, 254983, 254984, 255008,
	// 255009, 255010,
	// // 255042, 255068, 255071, 255073, 255074, 255075, 255076,  // these are runs with low statistics, excluded
	// 255079, 255082,
	// 255085, 255086//,
	// 255091, 255111, 255154, 255159, 255162, 255167, 255171, 255173, 255176,
	// 255177, 255180, 255182, 255240, 255242, 255247, 255248, 255249, 255251, 255252, 255253,
	// 255255, 255256, 255275, 255276, 255278, 255280, 255283, 255350, 255351, 255352, 255398,
	// 255402, 255407, 255440, 255442, 255447, 255463, 255465, 255466, 255467

	// };

	// LHC16i
	Int_t RunNumbers[] =
	{

		255616, 255615, 255614, 255592, 255591, 
		255582, 255577, 255543, 255542, 255540, 
		255538, 255537, 255535, 255534, 255533, 
		255515
	};

	Int_t nRuns = sizeof(RunNumbers) / sizeof(Int_t);
	cout << "We are trying to analyse " << nRuns << " runs" << endl;

	for (Int_t i = 0; i < nRuns; ++i)
		plugin->AddRunNumber(RunNumbers[i]);

// Int_t run_num[] = {139510, 139507, 139505, 139503, 139465, 139438, 139437, 139360, 139329, 139328, 139314, 139310, 139309, 139173, 139107, 139105, 139038, 139037, 139036, 139029, 139028, 138872, 138871, 138870, 138837, 138732, 138730, 138666, 138662, 138653, 138652, 138638, 138624, 138621, 138583, 138582, 138579, 138578, 138534, 138469, 138442, 138439, 138438, 138396, 138364, 138275, 138225, 138201, 138197, 138192, 138190, 137848, 137844, 137752, 137751, 137724, 137722, 137718, 137704, 137693, 137692, 137691, 137686, 137685, 137639, 137638, 137608, 137595, 137549, 137546, 137544, 137541, 137539, 137531, 137530, 137443, 137441, 137440, 137439, 137434, 137432, 137431, 137430, 137366, 137243, 137236, 137235, 137232, 137231, 137230, 137162, 137161, 137135};
// Int_t N = sizeof(run_num) / sizeof(Int_t);
// for (Int_t i = 0; i < N; ++i) plugin->AddRunNumber(run_num[i]);
// plugin->AddRunNumber(138534);

// plugin->AddRunNumber(137544);

	plugin->SetDefaultOutputs(kFALSE);
	plugin->SetOutputFiles("CaloCellsQA1.root CaloCellsQA2.root");

	plugin->SetGridWorkingDir("phosqa-16i-muon-calo-pass1-all");
	plugin->SetGridOutputDir("output");
// plugin->SetDefaultOutputs();
// Now this should be added in your AddTaskMacro.C

// plugin->SetAnalysisSource("ChargedTrack.h MyTaskHelper.cxx AliAnalysisTaskSimplePt.cxx");
// plugin->SetAdditionalLibs("ChargedTrack.h MyTaskHelper.h MyTaskHelper.cxx AliAnalysisTaskSimplePt.h AliAnalysisTaskSimplePt.cxx");

	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	// plugin->SetAnalysisSource("AliAnalysisTaskPi0QA.cxx");
	// plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so");// AliAnalysisTaskPi0QA.cxx AliAnalysisTaskPi0QA.h");

	plugin->SetAnalysisSource("AliAnalysisTaskCaloCellsQAPt.h");
	plugin->SetAdditionalLibs("libPWGGAPHOSTasks.so AliAnalysisTaskCaloCellsQAPt.h");


	plugin->SetAnalysisMacro("TaskQA.C");
	plugin->SetSplitMaxInputFileNumber(100);
	plugin->SetExecutable("TaskQA.sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName("TaskQA.jdl");
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
