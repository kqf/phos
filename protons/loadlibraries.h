void LoadAnalysisLibraries()
{

	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) 
	{
		cerr << "Fatal: There is no analysis manager" << endl;
		return;
	}

    gROOT->LoadMacro("AliPP13ClusterCuts.cxx+");
    gROOT->LoadMacro("AliPP13SelectionWeights.cxx+");
    gROOT->LoadMacro("AliPP13DetectorHistogram.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13PhotonSpectrumSelection.cxx+");
    gROOT->LoadMacro("AliPP13QualityPhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13ParticlesHistogram.cxx+");
    gROOT->LoadMacro("AliPP13PhotonTimecutStudySelection.cxx+");
    gROOT->LoadMacro("AliPP13PhysPhotonSelection.cxx+");
    gROOT->LoadMacro("AliPP13TagAndProbeSelection.cxx+");
    gROOT->LoadMacro("AliPP13PythiaInfoSelection.cxx+");
    gROOT->LoadMacro("AliPP13PhysPhotonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13NonlinearitySelection.cxx+");
    gROOT->LoadMacro("AliPP13EfficiencySelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13MesonSelectionMC.cxx+");
    gROOT->LoadMacro("AliPP13NonlinearityScanSelection.cxx+");
    gROOT->LoadMacro("AliPP13MixingSample.cxx+");
    gROOT->LoadMacro("AliAnalysisTaskPP13.cxx+");

	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());
	TString sources = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	plugin->SetAnalysisSource(
		sources +
	    "AliPP13ClusterCuts.cxx " +
	    "AliPP13SelectionWeights.cxx " +
	    "AliPP13DetectorHistogram.cxx " +
	    "AliPP13PhotonSelection.cxx " +
	    "AliPP13PhotonSelectionMC.cxx " +
	    "AliPP13PhotonSpectrumSelection.cxx " +
	    "AliPP13QualityPhotonSelection.cxx " +
	    "AliPP13ParticlesHistogram.cxx " +
	    "AliPP13PhysPhotonSelection.cxx " +
	    "AliPP13PhotonTimecutStudySelection.cxx " +
	    "AliPP13TagAndProbeSelection.cxx " +
	    "AliPP13PythiaInfoSelection.cxx " +
	    "AliPP13PhysPhotonSelectionMC.cxx " +
	    "AliPP13MesonSelectionMC.cxx " +
	    "AliPP13NonlinearitySelection.cxx " +
	    "AliPP13EfficiencySelectionMC.cxx " +
	    "AliPP13NonlinearityScanSelection.cxx " +
	    "AliPP13MixingSample.cxx " +
	    "AliAnalysisTaskPP13.cxx "
	);

	plugin->SetAdditionalLibs(
		libs +
		"libPWGGAPHOSTasks.so "	+
	    "AliPP13ClusterCuts.cxx " +
	    "AliPP13ClusterCuts.h " +
	    "AliPP13SelectionWeights.cxx " +
	    "AliPP13SelectionWeights.h " +
	    "AliPP13DetectorHistogram.cxx " +
	    "AliPP13DetectorHistogram.h " +
	    "AliPP13PhotonSelection.cxx " +
	    "AliPP13PhotonSelection.h " +
	    "AliPP13PhotonSelectionMC.cxx " +
	    "AliPP13PhotonSelectionMC.h " +
	    "AliPP13PhotonSpectrumSelection.cxx " +
	    "AliPP13PhotonSpectrumSelection.h " +
	    "AliPP13QualityPhotonSelection.cxx " +
	    "AliPP13QualityPhotonSelection.h " +
	    "AliPP13ParticlesHistogram.cxx " +
	    "AliPP13ParticlesHistogram.h " +
	    "AliPP13PhysPhotonSelection.cxx " +
	    "AliPP13PhysPhotonSelection.h " +
	    "AliPP13PhotonTimecutStudySelection.cxx " +
	    "AliPP13PhotonTimecutStudySelection.h " +
	    "AliPP13TagAndProbeSelection.cxx " +
	    "AliPP13TagAndProbeSelection.h " +
	    "AliPP13PhysPhotonSelectionMC.cxx " +
	    "AliPP13PhysPhotonSelectionMC.h " +
	    "AliPP13PythiaInfoSelection.cxx " +
	    "AliPP13PythiaInfoSelection.h " +
	    "AliPP13NonlinearitySelection.h " +
	    "AliPP13NonlinearitySelection.cxx " +
	    "AliPP13EfficiencySelectionMC.cxx " +
	    "AliPP13EfficiencySelectionMC.h " +
	    "AliPP13MesonSelectionMC.cxx " +
	    "AliPP13MesonSelectionMC.h " +
	    "AliPP13NonlinearityScanSelection.cxx " +
	    "AliPP13NonlinearityScanSelection.h " +
	    "AliPP13MixingSample.cxx " +
	    "AliPP13MixingSample.h " +
	    "AliAnalysisTaskPP13.cxx " +
	    "AliAnalysisTaskPP13.h " 
	);
}
