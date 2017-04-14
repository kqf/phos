#include "TROOT.h"
#include "AliAnalysisAlien.h"
#include "iostream"
#include "../datasets/values_for_dataset.h"	

using std::cout;
using std::endl;

AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString comment, Bool_t useJDL, Bool_t isMC)
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

	TString globaldir = isMC ? "/alice/sim/2010/" : "/alice/data/2010/";
	plugin->SetGridDataDir(globaldir + dir);
	cout << "/alice/data/2010/" + dir << endl;

	TString datasuffix = isMC ? "AOD172/" : "/*.";
	plugin->SetDataPattern("/" + reconstruction + datasuffix + "*/AliAOD.root");
	cout << "Data pattern " << "/" + reconstruction + "/*.*/AliAOD.root" << endl;

	// plugin->SetDataPattern("/" + reconstruction + "/AOD/*/AliAOD.root");
	// plugin->SetDataPattern("/muon_calo_pass1/*.*/AliESDs.root");
	if(!isMC)
		plugin->SetRunPrefix("000");

    std::vector<Int_t> v; // 
	values_for_dataset(v, dir);
	for (Int_t i = 0; i < v.size(); ++i)
		plugin->AddRunNumber(v[i]);

	plugin->SetDefaultOutputs(kFALSE);

	period.ToLower();
	plugin->SetGridWorkingDir("pp-phos-" + period + comment);
	plugin->SetGridOutputDir("output");


	plugin->AddIncludePath("-I$ALICE_PHYSICS/include");
	period.ReplaceAll('-', '_');

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
	plugin->SetFileForTestMode ( "filesmc.txt" );
	plugin->SetProofConnectGrid ( kFALSE );
	plugin->SetDropToShell(kFALSE);
	if (!plugin)
		cout << "Warning \n";
	return plugin;
}
