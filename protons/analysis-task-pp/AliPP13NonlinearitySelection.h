#ifndef ALIPP13NONLINEARITYSELECTION_H
#define ALIPP13NONLINEARITYSELECTION_H

// --- Custom header files ---
#include "AliPP13PhotonSelection.h"
#include "AliPP13SelectionWeights.h"
#include "AliPP13DetectorHistogram.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class AliPP13NonlinearitySelection: public AliPP13PhotonSelection
{
public:
	AliPP13NonlinearitySelection():
		AliPP13PhotonSelection(),
		fMassEnergy(),
		fWeights()
	{
	}

	AliPP13NonlinearitySelection(const char * name, const char * title, 
		AliPP13ClusterCuts cuts, AliPP13SelectionWeights w):
		AliPP13PhotonSelection(name, title, cuts),
		fMassEnergy(),
		fWeights(w)
	{
	}

	virtual void InitSelectionHistograms();

	~AliPP13NonlinearitySelection()
	{
		for(Int_t i = 0; i < 2; ++i)
		{
			if(fMassEnergy[i])
				delete fMassEnergy[i];
		}
	}
	
protected:
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags);

	AliPP13NonlinearitySelection(const AliPP13NonlinearitySelection &);
	AliPP13NonlinearitySelection & operator = (const AliPP13NonlinearitySelection &);

private:
	AliPP13DetectorHistogram * fMassEnergy[2]; //!
	AliPP13SelectionWeights fWeights;

	ClassDef(AliPP13NonlinearitySelection, 2)
};
#endif