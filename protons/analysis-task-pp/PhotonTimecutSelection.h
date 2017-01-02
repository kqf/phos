#ifndef PHOTONTIMECUTSELECTION_H
#define PHOTONTIMECUTSELECTION_H

// --- Custom header files ---
#include "PhysPhotonSelection.h"

// --- ROOT header files ---
#include "TH2F.h"


class PhotonTimecutSelection : public PhysPhotonSelection
{
public:

	PhotonTimecutSelection(): PhysPhotonSelection() {}
	PhotonTimecutSelection(const char * name, const char * title): PhysPhotonSelection(name, title) {}

	virtual void InitSummaryHistograms();
	void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	

protected:
	PhotonTimecutSelection(const PhotonTimecutSelection &);
	PhotonTimecutSelection & operator = (const PhotonTimecutSelection &);
	virtual Bool_t IsMainBC(const AliVCluster * clus) const;

private:
	ClassDef(PhotonTimecutSelection, 1)
};
#endif