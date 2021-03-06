#ifndef SOURCES_H
#define SOURCES_H


void LoadAnalysisLibraries()
{
	Int_t id = gClassTable->GetID("AliAnalysisTaskPP13");
	// Load analysis libraries for the older versions of aliphysics
	// without the task being manually added
	// if(id != -1)
		// return;

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr)
	{
		cerr << "Fatal: There is no analysis manager" << endl;
		return;
	}

	gInterpreter->LoadMacro("AliPP13AnalysisCluster.cxx+");
	gInterpreter->LoadMacro("AliPP13TriggerProperties.cxx+");
	gInterpreter->LoadMacro("AliPP13ClusterCuts.cxx+");
	gInterpreter->LoadMacro("AliPP13SelectionWeights.cxx+");
	gInterpreter->LoadMacro("AliPP13DetectorHistogram.cxx+");
	gInterpreter->LoadMacro("AliPP13PhysicsSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13PhotonSpectrumSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13SpectrumSelectionSimple.cxx+");
	gInterpreter->LoadMacro("AliPP13QualityPhotonSelection.cxx+");
	// TODO: Add to particle histogram
	gInterpreter->LoadMacro("AliPP13ParticlesHistogram.cxx+");
	gInterpreter->LoadMacro("AliPP13PhotonTimecutStudySelection.cxx+");
	gInterpreter->LoadMacro("AliPP13SpectrumSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13EpRatioSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13TagAndProbeSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13PythiaInfoSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13SpectrumSelectionMC.cxx+");
	gInterpreter->LoadMacro("AliPP13KaonToPionRatioMC.cxx+");
	gInterpreter->LoadMacro("AliPP13NonlinearitySelection.cxx+");
	gInterpreter->LoadMacro("AliPP13EfficiencySelectionMC.cxx+");
	gInterpreter->LoadMacro("AliPP13MesonSelectionMC.cxx+");
	gInterpreter->LoadMacro("AliPP13FeeddownSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13NonlinearityScanSelection.cxx+");
	gInterpreter->LoadMacro("AliPP13TriggerEfficiency.cxx+");
	gInterpreter->LoadMacro("AliPP13MixingSample.cxx+");
	gInterpreter->LoadMacro("AliAnalysisTaskPP13.cxx+");

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
		"AliPP13AnalysisCluster.cxx " +
		"AliPP13TriggerProperties.cxx " +
		"AliPP13ClusterCuts.cxx " +
		"AliPP13SelectionWeights.cxx " +
		"AliPP13DetectorHistogram.cxx " +
		"AliPP13PhysicsSelection.cxx " +
		"AliPP13PhotonSpectrumSelection.cxx " +
		"AliPP13SpectrumSelectionSimple.cxx " +
		"AliPP13QualityPhotonSelection.cxx " +
		"AliPP13ParticlesHistogram.cxx " +
		"AliPP13SpectrumSelection.cxx " +
		"AliPP13EpRatioSelection.cxx " +
		"AliPP13PhotonTimecutStudySelection.cxx " +
		"AliPP13TagAndProbeSelection.cxx " +
		"AliPP13PythiaInfoSelection.cxx " +
		"AliPP13SpectrumSelectionMC.cxx " +
		"AliPP13KaonToPionRatioMC.cxx " +
		"AliPP13MesonSelectionMC.cxx " +
		"AliPP13FeeddownSelection.cxx " +
		"AliPP13NonlinearitySelection.cxx " +
		"AliPP13EfficiencySelectionMC.cxx " +
		"AliPP13NonlinearityScanSelection.cxx " +
		"AliPP13TriggerEfficiency.cxx " +
		"AliPP13MixingSample.cxx " +
		"AliAnalysisTaskPP13.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
		"AliPP13AnalysisCluster.cxx " +
		"AliPP13AnalysisCluster.h " +
		"AliPP13TriggerProperties.cxx " +
		"AliPP13TriggerProperties.h " +
		"AliPP13ClusterCuts.cxx " +
		"AliPP13ClusterCuts.h " +
		"AliPP13SelectionWeights.cxx " +
		"AliPP13SelectionWeights.h " +
		"AliPP13DetectorHistogram.cxx " +
		"AliPP13DetectorHistogram.h " +
		"AliPP13PhysicsSelection.cxx " +
		"AliPP13PhysicsSelection.h " +
		"AliPP13PhotonSpectrumSelection.cxx " +
		"AliPP13PhotonSpectrumSelection.h " +
		"AliPP13SpectrumSelectionSimple.cxx " +
		"AliPP13SpectrumSelectionSimple.h " +
		"AliPP13QualityPhotonSelection.cxx " +
		"AliPP13QualityPhotonSelection.h " +
		"AliPP13ParticlesHistogram.cxx " +
		"AliPP13ParticlesHistogram.h " +
		"AliPP13SpectrumSelection.cxx " +
		"AliPP13SpectrumSelection.h " +
		"AliPP13EpRatioSelection.cxx " +
		"AliPP13EpRatioSelection.h " +
		"AliPP13PhotonTimecutStudySelection.cxx " +
		"AliPP13PhotonTimecutStudySelection.h " +
		"AliPP13TagAndProbeSelection.cxx " +
		"AliPP13TagAndProbeSelection.h " +
		"AliPP13SpectrumSelectionMC.cxx " +
		"AliPP13SpectrumSelectionMC.h " +
		"AliPP13KaonToPionRatioMC.cxx " +
		"AliPP13KaonToPionRatioMC.h " +
		"AliPP13PythiaInfoSelection.cxx " +
		"AliPP13PythiaInfoSelection.h " +
		"AliPP13NonlinearitySelection.h " +
		"AliPP13NonlinearitySelection.cxx " +
		"AliPP13EfficiencySelectionMC.cxx " +
		"AliPP13EfficiencySelectionMC.h " +
		"AliPP13MesonSelectionMC.cxx " +
		"AliPP13MesonSelectionMC.h " +
		"AliPP13FeeddownSelection.cxx " +
		"AliPP13FeeddownSelection.h " +
		"AliPP13NonlinearityScanSelection.cxx " +
		"AliPP13NonlinearityScanSelection.h " +
		"AliPP13TriggerEfficiency.cxx " +
		"AliPP13TriggerEfficiency.h " +
		"AliPP13MixingSample.cxx " +
		"AliPP13MixingSample.h " +
		"AliAnalysisTaskPP13.cxx " +
		"AliAnalysisTaskPP13.h "
	);
}

#endif
