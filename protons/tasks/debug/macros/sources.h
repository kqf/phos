void LoadAnalysisLibraries()
{

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
	{
		cerr << "Fatal: There is no analysis manager" << endl;
		return;
	}
	gROOT->LoadMacro("ClusterCuts.cxx+");
	gROOT->LoadMacro("SelectionWeights.cxx+");
	gROOT->LoadMacro("PhotonSelection.cxx+");
	gROOT->LoadMacro("EfficiencySelection.cxx+");
	gROOT->LoadMacro("MixingSample.cxx+");
	gROOT->LoadMacro("AnalysisTaskDebug.cxx+");

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
		"ClusterCuts.cxx " +
		"SelectionWeights.cxx " +
		"PhotonSelection.cxx " +
		"EfficiencySelection.cxx " +
		"MixingSample.cxx " +
		"AnalysisTaskDebug.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
		"ClusterCuts.cxx " +
		"ClusterCuts.h " +
		"SelectionWeights.cxx " +
		"SelectionWeights.h " +
		"PhotonSelection.cxx " +
		"PhotonSelection.h " +
		"EfficiencySelection.cxx " +
		"EfficiencySelection.h " +
		"MixingSample.cxx " +
		"MixingSample.h " +
		"AnalysisTaskDebug.cxx " +
		"AnalysisTaskDebug.h "
	);
}
