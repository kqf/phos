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
		fInvariantMass(),
		fClusters(0)
	{}

	PhysPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		GeneralPhotonSelection(name, title, ec, a, n, t),
		fInvariantMass(),
		fClusters(0)
	{}

	virtual ~PhysPhotonSelection()
	{
		// NB: Don't use this 
		// delete [] fInvariantMass;

		for(Int_t i = 0; i < 2; ++i)
			if (fInvariantMass[i]) delete fInvariantMass[i];

		// Don't delete fClusters, as ROOT will take 
		// care of it.
	}
	
	virtual void InitSelectionHistograms();

protected:
	virtual void FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	PhysPhotonSelection(const PhysPhotonSelection &);
	PhysPhotonSelection & operator = (const PhysPhotonSelection &);

private:
	DetectorHistogram * fInvariantMass[2]; //!
	TH1 * fClusters; //!
	ClassDef(PhysPhotonSelection, 2)
};
#endif