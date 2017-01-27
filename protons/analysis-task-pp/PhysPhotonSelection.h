#ifndef PHYSPHOTONSELECTION_H
#define PHYSPHOTONSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class PhysPhotonSelection : public GeneralPhotonSelection
{
public:
	PhysPhotonSelection(): GeneralPhotonSelection() {}
	PhysPhotonSelection(const char * name, const char * title): GeneralPhotonSelection(name, title) {}
	virtual void InitSelectionHistograms();

protected:

	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	PhysPhotonSelection(const PhysPhotonSelection &);
	PhysPhotonSelection & operator = (const PhysPhotonSelection &);

private:
	virtual Int_t AbsId(Int_t x, Int_t z, Int_t sm) const;
	ClassDef(PhysPhotonSelection, 2)
};
#endif