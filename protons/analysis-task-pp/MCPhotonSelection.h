#ifndef MCPHOTONSELECTION_H
#define MCPHOTONSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- ROOT system ---
#include <TClonesArray.h>
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>

class MCPhotonSelection: public GeneralPhotonSelection
{
public:
	MCPhotonSelection(): GeneralPhotonSelection() {}
	MCPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999): GeneralPhotonSelection(name, title, ec, a, n, t) {}
	virtual void InitSelectionHistograms();

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
    virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags);
    virtual void ConsiderGeneratedParticles(TClonesArray * particles);

	MCPhotonSelection(const MCPhotonSelection &);
	MCPhotonSelection & operator = (const MCPhotonSelection &);
	ClassDef(MCPhotonSelection, 2)
};
#endif