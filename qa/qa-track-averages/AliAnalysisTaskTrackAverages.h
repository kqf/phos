#include "AliEMCALGeometry.h"
#include "AliAnalysisTaskSE.h"

#include "AliVEvent.h"
#include "AliAODEvent.h"
#include "AliAODTrack.h"
#include "AliLog.h"
#include "TH1.h"
#include "TList.h"
#include "TString.h"

#include "iostream"
#include "algorithm"



class AliAnalysisTaskTrackAverages : public AliAnalysisTaskSE
{
public:
	AliAnalysisTaskTrackAverages(): AliAnalysisTaskSE(), fOutputContainer(0), fTracksTPC(0), fClustersEMCal(0), fEvents(0), fNRuns(0), fRuns(0) {}
	AliAnalysisTaskTrackAverages(const char * name): AliAnalysisTaskSE(name), fOutputContainer(0), fTracksTPC(0), fClustersEMCal(0), fEvents(0), fNRuns(0), fRuns(0)
	{
		DefineOutput(1, TList::Class());
	}

	virtual void UserCreateOutputObjects()
	{
		fOutputContainer = new TList();
		fOutputContainer->SetOwner(kTRUE);

		fEvents = new TH1F("hEvents", "Average number of TPC tracks", fNRuns, -0.5, fNRuns - 0.5);
		fTracksTPC = new TH1F("hTracksTPC", "Average number of TPC tracks", fNRuns, -0.5, fNRuns - 0.5);
		fClustersEMCal = new TH1F("hClustersEMCal", "Average number of TPC tracks", fNRuns, -0.5, fNRuns - 0.5);

		fOutputContainer->Add(fEvents);
		fOutputContainer->Add(fTracksTPC);
		fOutputContainer->Add(fClustersEMCal);

		PostData(1, fOutputContainer);
	}

	virtual void UserExec(Option_t * option)
	{
		AliVEvent * event = InputEvent();


		// Check event
		if (!event) return;
		Int_t bin = event->GetRunNumber();

		// Primary vertex
		AliVVertex * vertex = (AliVVertex *) event->GetPrimaryVertex();
		if (!vertex)
		{
			AliWarning("Could not get primary vertex");
			return;
		}

		if (TMath::Abs(vertex->GetZ()) > 10)
			return;

		Int_t nclusters = 0;
		for (Int_t i = 0; i < event->GetNumberOfCaloClusters(); i++)
		{
			AliVCluster * cluster = event->GetCaloCluster(i);
			if (!cluster)
			{
				AliWarning("Could not get cluster");
				return;
			}

			if (!cluster->IsEMCAL())
				continue;

			if (cluster->GetNCells() < 1)
				continue;

			if (cluster->E() < 0.3)
				continue;
			++nclusters;
		}
		fClustersEMCal->Fill(bin, nclusters);

		AliAODEvent * aod = dynamic_cast < AliAODEvent *>(event);
		if (!aod) return;

		Int_t ntracks = 0;
		for ( Int_t i = 0; i < aod->GetNumberOfTracks(); ++i)
		{
			AliAODTrack * track = static_cast < AliAODTrack * >(aod->GetTrack(i));
			if (! track ) continue ;
			++ntracks;
		}
		fTracksTPC->Fill(bin, ntracks);
		fEvents->Fill(bin);

		PostData(1, fOutputContainer);
	}


	virtual ~AliAnalysisTaskTrackAverages()
	{
		delete fOutputContainer;
	}


	void SetRuns(Int_t runs[], Int_t nruns)
	{
		if (fRuns) delete [] fRuns;

		if (nruns <= 0)
		{
			fNRuns = 0;
			return;
		}

		fNRuns = nruns;
		fRuns = new Int_t[nruns];

		for (Int_t i = 0; i < nruns; i++)
			fRuns[i] = runs[i];
	}

	Int_t findRunBin(Int_t run) const
	{
		for(Int_t i = 0; i < fNRuns; ++i)
			if(run == fRuns[i])
				return i;
		return -1;
	}

private:
	TList * fOutputContainer; //!
	TH1F * fTracksTPC; //!
	TH1F * fClustersEMCal; //!
	TH1F * fEvents; //!

	Int_t            fNRuns;    // number of entries in fRuns
	Int_t      *     fRuns;//[fNRuns] bad cells array


	ClassDef(AliAnalysisTaskTrackAverages, 1);
};
