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
	gROOT->LoadMacro("DetectorHistogram.cxx+");
	gROOT->LoadMacro("PhotonSelection.cxx+");
	gROOT->LoadMacro("PhotonSelectionMC.cxx+");
	gROOT->LoadMacro("PhotonSpectrumSelection.cxx+");
	gROOT->LoadMacro("QualityPhotonSelection.cxx+");
	// TODO: Add to particle histogram
	gROOT->LoadMacro("ParticlesHistogram.cxx+");
	gROOT->LoadMacro("PhotonTimecutStudySelection.cxx+");
	gROOT->LoadMacro("PhysPhotonSelection.cxx+");
	gROOT->LoadMacro("EpRatioSelection.cxx+");
	gROOT->LoadMacro("TagAndProbeSelection.cxx+");
	gROOT->LoadMacro("PythiaInfoSelection.cxx+");
	gROOT->LoadMacro("PhysPhotonSelectionMC.cxx+");
	gROOT->LoadMacro("KaonToPionRatioMC.cxx+");
	gROOT->LoadMacro("NonlinearitySelection.cxx+");
	gROOT->LoadMacro("EfficiencySelectionMC.cxx+");
	gROOT->LoadMacro("EfficiencySelectionSPMC.cxx+");
	gROOT->LoadMacro("MesonSelectionMC.cxx+");
	gROOT->LoadMacro("NonlinearityScanSelection.cxx+");
	gROOT->LoadMacro("MixingSample.cxx+");
	gROOT->LoadMacro("AliAnalysisTaskPP13.cxx+");

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
		"ClusterCuts.cxx " +
		"SelectionWeights.cxx " +
		"DetectorHistogram.cxx " +
		"PhotonSelection.cxx " +
		"PhotonSelectionMC.cxx " +
		"PhotonSpectrumSelection.cxx " +
		"QualityPhotonSelection.cxx " +
		"ParticlesHistogram.cxx " +
		"PhysPhotonSelection.cxx " +
		"EpRatioSelection.cxx " +
		"PhotonTimecutStudySelection.cxx " +
		"TagAndProbeSelection.cxx " +
		"PythiaInfoSelection.cxx " +
		"PhysPhotonSelectionMC.cxx " +
		"KaonToPionRatioMC.cxx " +
		"MesonSelectionMC.cxx " +
		"NonlinearitySelection.cxx " +
		"EfficiencySelectionMC.cxx " +
		"EfficiencySelectionSPMC.cxx " +
		"NonlinearityScanSelection.cxx " +
		"MixingSample.cxx " +
		"AliAnalysisTaskPP13.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
		"ClusterCuts.cxx " +
		"ClusterCuts.h " +
		"SelectionWeights.cxx " +
		"SelectionWeights.h " +
		"DetectorHistogram.cxx " +
		"DetectorHistogram.h " +
		"PhotonSelection.cxx " +
		"PhotonSelection.h " +
		"PhotonSelectionMC.cxx " +
		"PhotonSelectionMC.h " +
		"PhotonSpectrumSelection.cxx " +
		"PhotonSpectrumSelection.h " +
		"QualityPhotonSelection.cxx " +
		"QualityPhotonSelection.h " +
		"ParticlesHistogram.cxx " +
		"ParticlesHistogram.h " +
		"PhysPhotonSelection.cxx " +
		"PhysPhotonSelection.h " +
		"EpRatioSelection.cxx " +
		"EpRatioSelection.h " +
		"PhotonTimecutStudySelection.cxx " +
		"PhotonTimecutStudySelection.h " +
		"TagAndProbeSelection.cxx " +
		"TagAndProbeSelection.h " +
		"PhysPhotonSelectionMC.cxx " +
		"PhysPhotonSelectionMC.h " +
		"KaonToPionRatioMC.cxx " +
		"KaonToPionRatioMC.h " +
		"PythiaInfoSelection.cxx " +
		"PythiaInfoSelection.h " +
		"NonlinearitySelection.h " +
		"NonlinearitySelection.cxx " +
		"EfficiencySelectionMC.cxx " +
		"EfficiencySelectionMC.h " +
		"EfficiencySelectionSPMC.cxx " +
		"EfficiencySelectionSPMC.h " +
		"MesonSelectionMC.cxx " +
		"MesonSelectionMC.h " +
		"NonlinearityScanSelection.cxx " +
		"NonlinearityScanSelection.h " +
		"MixingSample.cxx " +
		"MixingSample.h " +
		"AliAnalysisTaskPP13.cxx " +
		"AliAnalysisTaskPP13.h "
	);
}
