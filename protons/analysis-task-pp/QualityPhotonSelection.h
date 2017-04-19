#ifndef QUALITYSELECTION_H
#define QUALITYSELECTION_H

// --- Custom header files ---
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
	QualityPhotonSelection(): GeneralPhotonSelection() {}
	QualityPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3): GeneralPhotonSelection(name, title, ec, a, n) {}
	virtual void InitSelectionHistograms();
    virtual Bool_t SelectEvent(const EventFlags & flgs);

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
    virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	QualityPhotonSelection(const QualityPhotonSelection &);
	QualityPhotonSelection & operator = (const QualityPhotonSelection &);

private:
	virtual Int_t AbsId(Int_t x, Int_t z, Int_t sm) const;
	ClassDef(QualityPhotonSelection, 2)
};
#endif