#ifndef TAGANDPROBESELECTION_H
#define TAGANDPROBESELECTION_H

// --- Custom header files ---
#include "PhotonSelection.h"
#include "DetectorHistogram.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class TagAndProbeSelection: public PhotonSelection
{
public:
	TagAndProbeSelection():
		PhotonSelection(),
		fMassEnergyAll(),
		fMassEnergyTOF()
	{
	}

	TagAndProbeSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		PhotonSelection(name, title, ec, a, n, t),
		fMassEnergyAll(),
		fMassEnergyTOF()
	{
	}

	virtual void InitSelectionHistograms();
	
protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags);

	TagAndProbeSelection(const TagAndProbeSelection &);
	TagAndProbeSelection & operator = (const TagAndProbeSelection &);
private:
	DetectorHistogram * fMassEnergyAll[2]; //!
	DetectorHistogram * fMassEnergyTOF[2]; //!

	ClassDef(TagAndProbeSelection, 2)
};
#endif