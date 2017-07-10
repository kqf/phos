#ifndef PHYSPHOTONSELECTION_H
#define PHYSPHOTONSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"
#include "DetectorHistogram.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class PhysPhotonSelection : public GeneralPhotonSelection
{
public:
	PhysPhotonSelection():
		GeneralPhotonSelection(),
		fInvariantMass(0),
		fMixedInvariantMass(0)
	{}

	PhysPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		GeneralPhotonSelection(name, title, ec, a, n, t),
		fInvariantMass(0),
		fMixedInvariantMass(0)
	{}

	virtual ~PhysPhotonSelection()
	{
		if (fInvariantMass) delete fInvariantMass;
		if (fMixedInvariantMass) delete fMixedInvariantMass;
	}
	
	virtual void InitSelectionHistograms();

protected:
	virtual void FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	PhysPhotonSelection(const PhysPhotonSelection &);
	PhysPhotonSelection & operator = (const PhysPhotonSelection &);

private:
	DetectorHistogram * fInvariantMass; //!
	DetectorHistogram * fMixedInvariantMass; //!
	ClassDef(PhysPhotonSelection, 2)
};
#endif