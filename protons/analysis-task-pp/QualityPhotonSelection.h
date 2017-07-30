#ifndef QUALITYSELECTION_H
#define QUALITYSELECTION_H

// --- Custom header files ---
#include "DetectorHistogram.h"
#include "PhotonSelection.h"

// --- ROOT system ---
#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>

#include <TObjArray.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class QualityPhotonSelection : public PhotonSelection
{
public:
	QualityPhotonSelection():
		PhotonSelection(),
		fClusterNXZ(),
		fClusterEXZ(),
		fClusterTime(0),
		fClusterEvsT(0),
		fClusterTimeMap(0),
		fClusterIdN(),
		fClusterIdE(),
		fMassPtA(),
		fZvertex(0),
		fNcellsE(0),
		fShapeE(0)
	{
	}

	QualityPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3):
		PhotonSelection(name, title, ec, a, n),
		fClusterNXZ(),
		fClusterEXZ(),
		fClusterTime(0),
		fClusterEvsT(0),
		fClusterTimeMap(0),
		fClusterIdN(),
		fClusterIdE(),
		fMassPtA(),
		fZvertex(0),
		fNcellsE(0),
		fShapeE(0)
	{
	}

	~QualityPhotonSelection()
	{
		// NB: Don't use "delete []", to supress warnings.
		//

		for(Int_t i = 0; i < 2; ++i)
		{
			if (fClusterNXZ[i]) delete fClusterNXZ[i];
			if (fClusterEXZ[i]) delete fClusterEXZ[i];
		}

		if (fClusterTime)    delete fClusterTime;
		if (fClusterEvsT)    delete fClusterEvsT;
		if (fClusterTimeMap) delete fClusterTimeMap;
	}

	virtual void InitSelectionHistograms();
	virtual Bool_t SelectEvent(const EventFlags & flgs);

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	QualityPhotonSelection(const QualityPhotonSelection &);
	QualityPhotonSelection & operator = (const QualityPhotonSelection &);

private:
	virtual Int_t AbsId(Int_t x, Int_t z, Int_t sm) const;

	DetectorHistogram * fClusterNXZ[2]; //!
	DetectorHistogram * fClusterEXZ[2]; //!
	DetectorHistogram * fClusterTime; //!
	DetectorHistogram * fClusterEvsT; //!
	DetectorHistogram * fClusterTimeMap; //!
	TH1F * fClusterIdN[2]; //!
	TH1F * fClusterIdE[2]; //!

	TH3F * fMassPtA[2]; //!
	TH1F * fZvertex; //!
	TH2F * fNcellsE; //!
	TH2F * fShapeE;  //!

	ClassDef(QualityPhotonSelection, 2)
};
#endif