#include "AliAnalysisTaskPHOSTriggerQA.h"

#include "AliVEvent.h"
#include "AliLog.h"

#include "TH1.h"
#include "TList.h"
#include "TString.h"

#include "iostream"
class AliAnalysisTaskPHOSTriggerQAPerRun : public AliAnalysisTaskPHOSTriggerQA
{
public:
	AliAnalysisTaskPHOSTriggerQAPerRun(): AliAnalysisTaskPHOSTriggerQA(), fOutputContainerAll(0) {}
	AliAnalysisTaskPHOSTriggerQAPerRun(const char * name, int level = -1): AliAnalysisTaskPHOSTriggerQA(name, level), fOutputContainerAll(0)
	{
		DefineOutput(1,TList::Class());
	}

	virtual void UserCreateOutputObjects()
	{
		fOutputContainerAll = new TList();
		fOutputContainerAll->SetOwner(kTRUE);
		fOutputContainerAll->Add( new TH1F("hEvents", "Total number of events", 1, 0, 1));
		PostData(1, fOutputContainerAll);
	}

	virtual void GetHistogramsForRun(Int_t run)
	{
		TString rname = Form("%d", run);

		TList * fOutputContainer = dynamic_cast<TList * >(fOutputContainerAll->FindObject(rname));
		if(fOutputContainer)
	 		return;

		fOutputContainer = dynamic_cast<TList * >(fOutputContainerAll->Last());
		if(fOutputContainer)
		{
			// Then we should clone old container
			// as AliAnalysisTaskPHOSTriggerQA::UserCreateOutputObjects deletes container if it's not zero
		 	fOutputContainerAll->Remove(fOutputContainer);
		 	TList * cloneContainer = dynamic_cast<TList *>(fOutputContainer->Clone());
		 	fOutputContainerAll->Add(cloneContainer);
		}

		AliAnalysisTaskPHOSTriggerQA::UserCreateOutputObjects();

		fOutputContainer = dynamic_cast<TList * >( AliAnalysisTaskPHOSTriggerQA::GetOutputData(1) );
		if(!fOutputContainer)
			AliFatal("AliAnalysisTaskPHOSTriggerQA task didn't produce any histograms in UserCreateOutputObjects");

		fOutputContainer->SetName(rname);
		fOutputContainerAll->Add(fOutputContainer);

		PostData(1, fOutputContainerAll);
	}

	virtual void UserExec(Option_t * option)
	{
		AliVEvent * event = InputEvent();
		if(!event) return;

		GetHistogramsForRun(event->GetRunNumber());
		AliAnalysisTaskPHOSTriggerQA::UserExec(option);

		TH1F * events = dynamic_cast<TH1F *> (fOutputContainerAll->FindObject("hEvents"));
		events->Fill(0.5);

		PostData(1, fOutputContainerAll);
	}

	virtual ~AliAnalysisTaskPHOSTriggerQAPerRun()
	{
		delete fOutputContainerAll;
	}

private:
	TList * fOutputContainerAll;
	ClassDef(AliAnalysisTaskPHOSTriggerQAPerRun, 1);
};