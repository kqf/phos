#include "../alienpluginsetup.h"	
#include "iostream"


using std::cout;
using std::endl;


AliAnalysisAlien * CreatePlugin(const char * pluginmode, TString inperiod, TString dpart, Bool_t useJDL, Bool_t isMC)
{

	Int_t pivot = inperiod.Index("_");

	TString ptbin = (pivot == -1) ? TString() : inperiod(pivot + 1, inperiod.Length());
	TString period = (pivot == -1) ? inperiod : inperiod(0, pivot);


	TString fperiod = isMC ? inperiod.ReplaceAll("_", "/") : period; // fancy slicing

	// Maximal size of the dataset that shouldn't be slitted on two halves
	Int_t msize = 100;	

	// Use default setup for the plugin
	AliAnalysisAlien * plugin = GetPlugin(pluginmode, period, dpart, useJDL, isMC, msize);

	// Setup data path
	TString year = inperiod.Contains('LHC15') ? "2015" : "2014";

	TString globaldir = isMC ? TString("/alice/sim/") + year + "/" : TString("/alice/data/2010/");
	plugin->SetGridDataDir(globaldir + fperiod);

	TString reconstruction = isMC ? "AOD/" : "pass4/AOD172/";
	plugin->SetDataPattern("/" + reconstruction + "*/AliAOD.root");

	if(ptbin.Length())
	{
		cout << "* * * * * * * * * * *" << endl;
		cout << ptbin << endl;
		cout << "* * * * * * * * * * *" << endl;
		plugin->SetExecutable(TString(plugin->GetExecutable()).ReplaceAll(".sh", ptbin + ".sh"));
		plugin->SetGridWorkingDir(TString(plugin->GetGridWorkingDir()) + "/" + ptbin);
		plugin->SetOverwriteMode(kTRUE);
	}

	return plugin;
}
