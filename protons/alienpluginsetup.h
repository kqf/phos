#include "AliAnalysisAlien.h"
#include "iostream"
#include "datasets/values_for_dataset.h"

using std::cout;
using std::endl;

AliAnalysisAlien * GetPlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC, Int_t msize = 200)
{
	if (period.Length() < 6)
		cerr << "Error: Wrong run period (too short)" << period << endl;

	AliAnalysisAlien * plugin = new AliAnalysisAlien();
	plugin->SetOverwriteMode(kTRUE);

	plugin->SetMergeViaJDL(useJDL);
	plugin->SetOutputToRunNo(kTRUE);
	plugin->SetKeepLogs(kTRUE);


	plugin->SetRunMode(pluginmode);

	plugin->SetAPIVersion("V1.1x");
	plugin->SetAliPhysicsVersion("vAN-20170222-1");


	plugin->SetExecutableCommand("aliroot");
	plugin->SetExecutableArgs("-b -q -x");

	plugin->SetCheckCopy(kFALSE);


	if (!isMC)
		plugin->SetRunPrefix("000");
	
	std::vector<Int_t> v; //
	values_for_dataset(v, period);

	// This is to avoid limitation on grid jobs
	//

	// Int_t msize = 200;
	Int_t start = (dpart.Contains("first") || v.size() <  msize) ? 0 : v.size() / 2;
	Int_t stop =  (dpart.Contains("first") && !(v.size() <  msize)) ? v.size() / 2 : v.size();


	TString info = dpart.Contains("first") ? "first" :  "second";

	// Don't add any endings if we have only one 
	if(!TString(pluginmode).Contains("terminate"))
	{
		// Repeat the message othervise it's not visible in the logs.
		for (int i = 0; i < 5; ++i)
			cout << "Important: you are running only on " << info << " part of the dataset. " << endl;
	}

	
	// Terminate all datasets simultaneously
	if (TString(pluginmode).Contains("terminate"))
	{
		start = 0;
		stop = v.size();
	}


	for (Int_t i = start; i < stop; ++i)
		plugin->AddRunNumber(v[i]);

	plugin->SetDefaultOutputs(kFALSE);
	// plugin->SetOutputFiles("CaloCellsQA2.root TriggerQA.root");
	// plugin->SetOutputFiles("TriggerQA.root");

	period.ToLower();
	plugin->SetGridWorkingDir("pp-phos-" + period);
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

	plugin->SetAnalysisMacro(TString("TaskPP_") + period + ".C");
	plugin->SetSplitMaxInputFileNumber(100);


	// Do not use ending: it will fail your jobs on grid at terminate stage.
	plugin->SetExecutable(TString("TaskPP_") + period + ".sh");

	plugin->SetTTL(30000);
	plugin->SetInputFormat("xml-single");
	plugin->SetJDLName(TString("TaskPP_") + period + ".jdl");
	plugin->SetPrice(1);
	plugin->SetSplitMode("se");
	plugin->SetProofCluster ( "alice-caf.cern.ch" );
	plugin->SetProofDataSet ( "/alice/data/LHC10h_000138150_p2" );
	plugin->SetProofReset ( 0 );
	plugin->SetNproofWorkers ( 0 );


	plugin->SetAliRootMode ( "default" );
	plugin->SetClearPackages ( kFALSE );
	plugin->SetProofConnectGrid ( kFALSE );
	plugin->SetDropToShell(kFALSE);
	return plugin;
}
