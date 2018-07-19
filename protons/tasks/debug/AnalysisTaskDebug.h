#ifndef ANALYSISTASKDEBUG_H
#define ANALYSISTASKDEBUG_H

// --- ROOT system ---
#include <TString.h>
#include <TClonesArray.h>

// --- AliRoot header files ---
#include <AliAnalysisTaskSE.h>

// --- Custom libraries ---
#include "PhotonSelection.h"
#include "MixingSample.h"

class AnalysisTaskDebug : public AliAnalysisTaskSE
{

public:
	enum {kMinModule = 1, kMaxModule=4};
	AnalysisTaskDebug();
	AnalysisTaskDebug(const char * name, TList * selections, Int_t nmix = 100);
	virtual ~AnalysisTaskDebug();

	void   UserCreateOutputObjects();
	void   UserExec(Option_t *);
	void   Terminate(Option_t *);

	TList * GetSelections() { return fSelections; }

protected:
	TClonesArray * GetMCParticles(const AliVEvent * event) const;
	AnalysisTaskDebug & operator =(const AnalysisTaskDebug &);
	AnalysisTaskDebug(const AnalysisTaskDebug & c);

private:
	AliPP13MixingSample * fPreviousEvents;
	TList * fSelections;     // analysis instance
	Int_t fNMixedEvents;     // number of events used for mixing

	ClassDef(AnalysisTaskDebug, 2);
};

#endif