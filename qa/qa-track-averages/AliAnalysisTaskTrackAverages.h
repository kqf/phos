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
	AliAnalysisTaskTrackAverages():
		AliAnalysisTaskSE(),
		fOutputContainer(0),
		fTracksTPC(0),
		fClustersEMCal(0),
		fETracksTPC(0),
		fEClustersEMCal(0),
		fEvents(0),
		fNRuns(0),
		fRuns(0)
	{}

	AliAnalysisTaskTrackAverages(const char * name):
		AliAnalysisTaskSE(name),
		fOutputContainer(0),
		fTracksTPC(0),
		fClustersEMCal(0),
		fETracksTPC(0),
		fEClustersEMCal(0),
		fEvents(0),
		fNRuns(0),
		fRuns(0)
	{
		DefineOutput(1, TList::Class());
	}

	virtual void UserCreateOutputObjects()
	{
		fOutputContainer = new TList();
		fOutputContainer->SetOwner(kTRUE);

		fEvents = new TH1F("hEvents", "Number of events per run index", fNRuns, -0.5, fNRuns - 0.5);

		fTracksTPC = new TH1F("hTracksTPC", "Total number of TPC tracks", fNRuns, -0.5, fNRuns - 0.5);
		fClustersEMCal = new TH1F("hClustersEMCal", "Total number of EMCal clusters", fNRuns, -0.5, fNRuns - 0.5);

		fETracksTPC = new TH1F("hETracksTPC", "Average energy of TPC tracks per event;; E, GeV", fNRuns, -0.5, fNRuns - 0.5);
		fEClustersEMCal = new TH1F("hEClustersEMCal", "Average energy of EMCal clusters per event;; E, GeV", fNRuns, -0.5, fNRuns - 0.5);


		fOutputContainer->Add(DecorateHistogram(fEvents));
		fOutputContainer->Add(DecorateHistogram(fTracksTPC));
		fOutputContainer->Add(DecorateHistogram(fClustersEMCal));
		fOutputContainer->Add(DecorateHistogram(fETracksTPC));
		fOutputContainer->Add(DecorateHistogram(fEClustersEMCal));


		PostData(1, fOutputContainer);
	}

	virtual void UserExec(Option_t * option)
	{
		AliVEvent * event = InputEvent();


		// Check event
		if (!event) return;


		Int_t run = event->GetRunNumber();

		cout << "run: " << run << endl;
		run = fRuns[5];

		Int_t bin = findRunBin(run);

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
		Int_t energy_emc = 0;
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
			energy_emc += cluster->E();
		}
		fClustersEMCal->Fill(bin, nclusters);
		if (nclusters)
			fEClustersEMCal->Fill(bin, energy_emc / nclusters);

		AliAODEvent * aod = dynamic_cast < AliAODEvent *>(event);
		if (!aod) return;

		Int_t ntracks = 0;
		Int_t energy_tpc = 0;
		for ( Int_t i = 0; i < aod->GetNumberOfTracks(); ++i)
		{
			AliAODTrack * track = static_cast < AliAODTrack * >(aod->GetTrack(i));
			if (! track ) continue ;
			++ntracks;
			energy_tpc += track->E();
		}

		fTracksTPC->Fill(bin, ntracks);
		if (ntracks)
			fETracksTPC->Fill(bin, energy_tpc / ntracks);
		fEvents->Fill(bin);

		PostData(1, fOutputContainer);
	}

	TH1* DecorateHistogram(TH1 *histo) const
	{
		for (Int_t i = 0; i < fNRuns; i++)
			histo->GetXaxis()->SetBinLabel(i + 1, Form("%d", fRuns[i]));
		histo->LabelsOption("v");
		return histo;
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
		for (Int_t i = 0; i < fNRuns; ++i)
			if (run == fRuns[i])
				return i;
		return -1;
	}

private:
	TList * fOutputContainer; //!
	TH1F * fTracksTPC; //!
	TH1F * fETracksTPC; //!
	TH1F * fEClustersEMCal; //!
	TH1F * fClustersEMCal; //!

	TH1F * fEvents; //!

	Int_t            fNRuns;    // number of entries in fRuns
	Int_t      *     fRuns;//[fNRuns] bad cells array


	ClassDef(AliAnalysisTaskTrackAverages, 1);
};
