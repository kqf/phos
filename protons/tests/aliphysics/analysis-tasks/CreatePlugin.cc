#include "../../../setup/alien.h"
#include "../../../setup/values_for_dataset.h"
#include "iostream"

using std::cout;
using std::endl;

AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC)
{
	// Maximal size of the dataset that shouldn't be slitted on two halves
	Int_t msize = 80;	

	// Use default setup for the plugin
	AliAnalysisGrid * plugin = GetPlugin(pluginmode, period, dpart, useJDL, isMC, msize);
	std::vector<Int_t> v; //
	values_for_dataset(v, period, "../../../datasets/");
	for (UInt_t i = 0; i < v.size(); ++i)
		plugin->AddRunNumber(v[i]);	
	// Extract period and reconstruction pass
	TString dir = period.Contains("_extra") ? period : TString(period, isMC ? 10 : 6); // fancy slicing
	
	TString reconstruction(period);
	reconstruction.ReplaceAll(dir + (reconstruction.Contains(dir + "-") ? "-" : "") , "");
	reconstruction.ReplaceAll("-", "_");

	TString globaldir = isMC ? "/alice/sim/2017/" : "/alice/data/2016/";
	plugin->SetGridDataDir(globaldir + dir);
	cout << "/alice/data/2016/" + dir << endl;

	TString datasuffix = isMC ? "AOD/" : "/*.";
	plugin->SetDataPattern("/" + reconstruction + datasuffix + "*/AliAOD.root");
	cout << "Data pattern " << "/" + reconstruction + "/*.*/AliAOD.root" << endl;

	const char * testfile = isMC ? "../../../datasets/filesmc.txt": "../../../datasets/files.txt";
	plugin->SetFileForTestMode(testfile);
	return plugin;
}
