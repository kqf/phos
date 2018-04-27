#ifndef ALIPP13EPRATIOSELECTION_H
#define ALIPP13EPRATIOSELECTION_H

// --- Custom header files ---
#include "AliPP13PhotonSelection.h"
#include "AliPP13DetectorHistogram.h"
#include "AliPP13SelectionWeights.h"
	

// --- ROOT system ---
#include <TObjArray.h>
#include <TVector3.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class AliPP13EpRatioSelection : public AliPP13PhotonSelection
{
public:
	AliPP13EpRatioSelection():
		AliPP13PhotonSelection(),
		fEpP(),
		fEpPt(),
		fTPCSignal()
	{}

	AliPP13EpRatioSelection(const char * name, const char * title, AliPP13ClusterCuts cuts,
		AliPP13SelectionWeights * w):
		AliPP13PhotonSelection(name, title, cuts, w),
		fEpP(),
		fEpPt(),
		fTPCSignal()
	{}

	virtual ~AliPP13EpRatioSelection()
	{
		// NB: Don't use this 
		// delete [] fInvariantMass;
		for(Int_t i = 0; i < 2; ++i)
		{
			if (fEpP[i]) 
				delete fEpP[i];

			if (fEpPt[i]) 
				delete fEpPt[i];
		}

		// Don't delete fClusters, as ROOT will take 
		// care of it.
	}
	
	virtual void InitSelectionHistograms();

	// NB: It actually doesn't fill Pi0Mass
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags); 

protected:
	TVector3 LocalPosition(const AliVCluster * clus) const;
	virtual void FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags);

	AliPP13EpRatioSelection(const AliPP13EpRatioSelection &);
	AliPP13EpRatioSelection & operator = (const AliPP13EpRatioSelection &);
private:
	AliPP13DetectorHistogram * fEpP[2]; //!
	AliPP13DetectorHistogram * fEpPt[2]; //!
	TH2 * fTPCSignal[4]; //!
	ClassDef(AliPP13EpRatioSelection, 2)
};
#endif