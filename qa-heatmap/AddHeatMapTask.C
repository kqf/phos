void AddHeatMapTask(Int_t badcells[], Int_t nbad)
{
    gROOT->LoadMacro("AliAnalysisTaskPHOSHeatMap.h+g");
	AliAnalysisManager * mgr = AliAnalysisManager::GetAnalysisManager();
	if (!mgr) return;

	AliAnalysisTaskPHOSHeatMap * task = new AliAnalysisTaskPHOSHeatMap("PhosHeatMap");
	task->SelectCollisionCandidates(AliVEvent::kINT7);
	task->SetBadCells(badcells, nbad);
	
	mgr->AddTask(task);

	mgr->ConnectInput (task, 0, mgr->GetCommonInputContainer());
	coutput = mgr->CreateContainer("HeatMaps",
	                               TList::Class(),
	                               AliAnalysisManager::kOutputContainer,
	                               AliAnalysisManager::GetCommonFileName());
	mgr->ConnectOutput(task, 1, coutput);


	AliAnalysisAlien * plugin = dynamic_cast<AliAnalysisAlien * >(mgr->GetGridHandler());

	TString souces = plugin->GetAnalysisSource();
	TString libs   = plugin->GetAdditionalLibs();
	TString output = plugin->GetOutputFiles();

	plugin->SetAnalysisSource(souces + " AliAnalysisTaskPHOSHeatMap.h ");
	plugin->SetAdditionalLibs(libs + " AliAnalysisTaskPHOSHeatMap.h ");
	plugin->SetOutputFiles(output + " AnalysisResults.root ");

	return task;	
}
