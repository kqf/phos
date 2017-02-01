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
	PhotonTimecutSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Int_t t = 12.5e-9): 
	GeneralPhotonSelection(name, title, ec, a, n),
	fTimingCutPair(t)
	{}
	virtual void InitSelectionHistograms();

protected:

	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	PhotonTimecutSelection(const PhotonTimecutSelection &);
	PhotonTimecutSelection & operator = (const PhotonTimecutSelection &);
	virtual Bool_t IsMainBC(const AliVCluster * clus) const;

	// This one should't be used for selection,
	// it should be applied for combinations.
	//
	Float_t fTimingCutPair;
private:
	ClassDef(PhotonTimecutSelection, 1)
};
#endif