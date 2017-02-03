TString AddAnalysisTaskTrackAverages(Int_t runs[], Int_t nruns)
{
    gROOT->LoadMacro("AliAnalysisTaskTrackAverages.h+g");
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

	AliAnalysisTaskTrackAverages * task = new AliAnalysisTaskTrackAverages("TrackAverages");
	task->SelectCollisionCandidates(AliVEvent::kINT7);
	task->SetRuns(runs, nruns);
	
	mgr->AddTask(task);

	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	coutput = mgr->CreateContainer("TrackAverages",
	                               TList::Class(),
	                               AliAnalysisManager::kOutputContainer,
	                               "TrackAverages.root");
	mgr->ConnectOutput(task, 1, coutput);


	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());

	TString souces = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	TString output = plugin->GetOutputFiles();

	plugin->SetAnalysisSource(souces + " AliAnalysisTaskTrackAverages.h ");
	plugin->SetAdditionalLibs(libs + " AliAnalysisTaskTrackAverages.h ");

	return " TrackAverages.root ";
}
