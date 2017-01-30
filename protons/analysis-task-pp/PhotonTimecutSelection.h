#ifndef PHOTONTIMECUTSELECTION_H
#define PHOTONTIMECUTSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- ROOT header files ---
#include "TH2F.h"


class PhotonTimecutSelection : public GeneralPhotonSelection
{
public:

	PhotonTimecutSelection(): GeneralPhotonSelection() {}
	PhotonTimecutSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3): GeneralPhotonSelection(name, title, ec, a, n) {}

	virtual void InitSelectionHistograms();
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