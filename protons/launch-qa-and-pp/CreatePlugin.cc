#include "../alienpluginsetup.h"	
#include "iostream"

using std::cout;
using std::endl;

AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC)
{
	// Maximal size of the dataset that shouldn't be slitted on two halves
	Int_t msize = 50;	

	// Use default setup for the plugin
	AliAnalysisGrid * plugin = GetPlugin(pluginmode, period, dpart, useJDL, isMC, msize);

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

	plugin->SetFileForTestMode ( "filesmc.txt" );
	return plugin;
}
