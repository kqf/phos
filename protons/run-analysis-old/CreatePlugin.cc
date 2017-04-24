#include "../alienpluginsetup.h"	
#include "iostream"


using std::cout;
using std::endl;


AliAnalysisGrid * CreatePlugin(const char * pluginmode, TString period, TString dpart, Bool_t useJDL, Bool_t isMC)
{

	// Extract period and reconstruction pass
	TString dir(period, isMC ? 9 : 6); // fancy slicing

	// Use default setup for the plugin
	AliAnalysisGrid * plugin = GetPlugin(pluginmode, dir, dpart, useJDL, isMC);


	TString reconstruction(period);
	reconstruction.ReplaceAll(dir + (reconstruction.Contains(dir + "-") ? "-" : "") , "");
	reconstruction.ReplaceAll("-", "_");

	TString globaldir = isMC ? "/alice/sim/2010/" : "/alice/data/2010/";
	plugin->SetGridDataDir(globaldir + dir);
	cout << "/alice/data/2010/" + dir << endl;

	TString datasuffix = isMC ? "AOD172/" : "/*.";
	plugin->SetDataPattern("/" + reconstruction + datasuffix + "*/AliAOD.root");
	cout << "Data pattern " << "/" + reconstruction + "/*.*/AliAOD.root" << endl;

	return plugin;
}
