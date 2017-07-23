#ifndef QUALITYSELECTION_H
#define QUALITYSELECTION_H

// --- Custom header files ---
#include "DetectorHistogram.h"
#include "GeneralPhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class QualityPhotonSelection : public GeneralPhotonSelection
{
public:
	QualityPhotonSelection():
		GeneralPhotonSelection(),
		fClusterNXZ(),
		fClusterEXZ(),
		fClusterTime(0),
		fClusterEvsT(0),
		fClusterTimeMap(0),
		fClusterIdN(),
		fClusterIdE()
	{
	}

	QualityPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3):
		GeneralPhotonSelection(name, title, ec, a, n),
		fClusterNXZ(),
		fClusterEXZ(),
		fClusterTime(0),
		fClusterEvsT(0),
		fClusterTimeMap(0),
		fClusterIdN(),
		fClusterIdE()
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

	ClassDef(QualityPhotonSelection, 2)
};
#endif