#include "../alienpluginsetup.h"	
#include "iostream"

using std::cout;
using std::endl;

AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC)
{
	// Crash run.C macro if wrong input
	if(!isMC)
		return 0;

	// Use default setup for the plugin
	AliAnalysisGrid * plugin = GetPlugin(pluginmode, "single-pi0", dpart, useJDL, isMC, 0);

	// Extract period and reconstruction pass

	// TODO: Use cl environment instead
	TString path("/alice/cern.ch/user/o/okovalen/single-pi0-production/output/");

	cout << "RUn number " << period << endl;
	plugin->AddRunNumber(period.Atoi());
	plugin->SetGridDataDir(path);
	plugin->SetDataPattern(path + period + "/" + "*/AliAOD.root");
	plugin->SetFileForTestMode ("filesmc.txt");
	return plugin;
}
