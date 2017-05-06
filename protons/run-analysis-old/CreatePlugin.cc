#include "../alienpluginsetup.h"	
#include "iostream"


using std::cout;
using std::endl;


AliAnalysisAlien * CreatePlugin(const char * pluginmode, TString inperiod, TString dpart, Bool_t useJDL, Bool_t isMC)
{

	Int_t pivot = inperiod.Index("_");
	TString ptbin = inperiod(pivot + 1, inperiod.Length());
	TString period = inperiod(0, pivot);

	// Extract period and reconstruction pass
	TString dir = isMC ? inperiod.ReplaceAll("_", "/") : TString(period, isMC ? 9 : 6); // fancy slicing

	// Use default setup for the plugin
	AliAnalysisAlien * plugin = GetPlugin(pluginmode, period, dpart, useJDL, isMC);


	TString reconstruction = isMC ? "": period;
	reconstruction.ReplaceAll(dir + (reconstruction.Contains(dir + "-") ? "-" : "") , "");
	reconstruction.ReplaceAll("-", "_");

	TString globaldir = isMC ? "/alice/sim/2015/" : "/alice/data/2010/";
	plugin->SetGridDataDir(globaldir + dir);

	cout << globaldir + dir << endl;

	TString datasuffix = isMC ? "AOD/" : "/*.";
	plugin->SetDataPattern("/" + reconstruction + datasuffix + "*/AliAOD.root");
	cout << "Data pattern " << "/" + reconstruction + "/*.*/AliAOD.root" << endl;

	plugin->SetExecutable(TString(plugin->GetExecutable()).ReplaceAll(".sh", ptbin + ".sh"));
	// plugin->SetGridOutputDir(TString(plugin->GetGridOutputDir()) + ptbin);
	plugin->SetGridWorkingDir(TString(plugin->GetGridWorkingDir()) + "/" + ptbin);
	plugin->SetOverwriteMode(kTRUE);
	return plugin;
}
