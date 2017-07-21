#ifndef PHOTONTIMECUTSELECTION_H
#define PHOTONTIMECUTSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"
#include "DetectorHistogram.h"

// --- ROOT header files ---
#include "TH2F.h"


class PhotonTimecutSelection : public GeneralPhotonSelection
{
public:

	PhotonTimecutSelection():
		GeneralPhotonSelection(),
		fTimingCutPair(999999),
		fMassPt(),
		fMassPtMainMain(),
		fMassPtMainPileup(),
		fMassPtPileupPileup()
	{}

	PhotonTimecutSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Int_t t = 12.5e-9):
		GeneralPhotonSelection(name, title, ec, a, n, 99999), // Pass infinite (99999) cut to select all clusters
		fTimingCutPair(t),                                   // Use timing cut for pair of clusters
		fMassPt(),
		fMassPtMainMain(),
		fMassPtMainPileup(),
		fMassPtPileupPileup()

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

	DetectorHistogram * fMassPt[2];             //!
	DetectorHistogram * fMassPtMainMain[2];     //!
	DetectorHistogram * fMassPtMainPileup[2];   //!
	DetectorHistogram * fMassPtPileupPileup[2]; //!

	ClassDef(PhotonTimecutSelection, 1)
};
#endif