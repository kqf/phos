#ifndef ALIANALYSISTASKPROMPT_H
#define ALIANALYSISTASKPROMPT_H

// --- ROOT system ---
#include <TString.h>

// --- AliRoot header files ---
#include <AliAnalysisTaskSE.h>

// --- Custom libraries ---
#include "PhotonSelection.h"

class EventFlags;
class AliAnalysisTaskPrompt : public AliAnalysisTaskSE
{
public:
	enum {kMinModule = 1, kMaxModule=4};
	AliAnalysisTaskPrompt();
	AliAnalysisTaskPrompt(const char * name);
	virtual ~AliAnalysisTaskPrompt();

	void   UserCreateOutputObjects();
	void   UserExec(Option_t *);
	void   Terminate(Option_t *);

	void SetBadCells(Int_t badcells[], Int_t nbad);
	void SetBadMap(const char * filename);
	TList * GetSelections() { return fSelections; }
protected:
	Bool_t EventSelected(const AliVEvent * event, EventFlags & eprops) const;
	Bool_t IsClusterBad(AliVCluster * clus) const;
	Bool_t CellInPhos(Int_t absId, Int_t & sm, Int_t & ix, Int_t & iz) const;

	AliAnalysisTaskPrompt & operator =(const AliAnalysisTaskPrompt &);
	AliAnalysisTaskPrompt(const AliAnalysisTaskPrompt & c);

private:
	TList * fSelections;     // analysis instance
	TH2I  * fPHOSBadMap[kMaxModule - kMinModule + 1];  // bad channel maps
	Int_t fNBad;             // number of entries in fBadCells
	Int_t * fBadCells;       //[fNBad] bad cells array

	ClassDef(AliAnalysisTaskPrompt, 2);
};

#endif