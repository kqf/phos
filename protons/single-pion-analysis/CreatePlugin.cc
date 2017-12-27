#include "../../setup/alien.h"	
#include "iostream"
#include "AliAnalysisManager.h"


using std::cout;
using std::endl;

AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC = kTRUE)
{
	// Maximal size of the dataset that shouldn't be slitted on two halves
	Int_t msize = 80;

	// Use default setup for the plugin
	AliAnalysisGrid * plugin = GetPlugin(pluginmode, period, dpart, useJDL, isMC, msize);
	TString dir = period.Contains("_extra") ? period : TString(period, isMC ? 10 : 6); // fancy slicing

	// DataDir = /alice/sim/2017/LHC17i7b2/ , DataPettern = /*/AliAOD.root
	TString datadir = "/alice/sim/2017/" + dir + "/";
	plugin->SetGridDataDir(datadir);

	TString datapattern = "/*/AliAOD.root";
	plugin->SetDataPattern(datapattern);

	cout << "DataDir " <<  datadir << " pattern " << datapattern << endl;

	plugin->SetFileForTestMode("../datasets/filesmc.txt");
    plugin->SetOutputFiles(AliAnalysisManager::GetCommonFileName());
    
    //plugin->SetUseSubmitPolicy();
	return plugin;
}
