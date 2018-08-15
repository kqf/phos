#ifndef ALIANALYSISTASKTRACKAVERAGES_H
#define ALIANALYSISTASKTRACKAVERAGES_H

// --- ROOT system ---
#include "TList.h"
#include "TH1.h"

// --- AliRoot header files ---
#include "AliAnalysisTaskSE.h"
#include "AliVEvent.h"


// --- Custom libraries ---
// None


class AliAnalysisTaskTrackAverages : public AliAnalysisTaskSE
{
public:
	AliAnalysisTaskTrackAverages();
	AliAnalysisTaskTrackAverages(const char * name);
	virtual ~AliAnalysisTaskTrackAverages()
	{
		delete fOutputContainer;
	}

	virtual void UserCreateOutputObjects();
	virtual void UserExec(Option_t * option);
	void SetRuns(Int_t runs[], Int_t nruns);

protected:
	TH1* DecorateHistogram(TH1 *histo) const;
	Int_t findRunBin(Int_t run) const;

	void AnalysePHOSClusters(const AliVEvent * event, Int_t bin);
	void AnalyseEMCalClusters(const AliVEvent * event, Int_t bin);
	void AnalyseChargedTracks(const AliVEvent * event, Int_t bin);

protected:
	TList * fOutputContainer; //!
	TH1F * fHybridTPC; //!
	TH1F * fComplementaryTPC; //!
	TH1F * fTracksTPC; //!
	TH1F * fETracksTPC; //!
	TH1F * fClustersEMCal; //!
	TH1F * fEClustersEMCal; //!
	TH1F * fClustersPHOS; //!
	TH1F * fEClustersPHOS; //!	
	TH1F * fEventClustersPHOS; //!	
	TH1F * fEvents; //!

	Int_t            fNRuns;    // number of entries in fRuns
	Int_t      *     fRuns;//[fNRuns] bad cells array


	ClassDef(AliAnalysisTaskTrackAverages, 1);
};

#endif