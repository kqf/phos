#ifndef PHYSPHOTONSELECTION_H
#define PHYSPHOTONSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class PhysPhotonSelection : public GeneralPhotonSelection
{
public:
	PhysPhotonSelection(): GeneralPhotonSelection() {}
	PhysPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3): GeneralPhotonSelection(name, title, ec, a, n) {}
	virtual void InitSelectionHistograms();

protected:

	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	PhysPhotonSelection(const PhysPhotonSelection &);
	PhysPhotonSelection & operator = (const PhysPhotonSelection &);

private:
	ClassDef(PhysPhotonSelection, 2)
};
#endif