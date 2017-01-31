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

class PhotonSpectrumSelection : public GeneralPhotonSelection
{
public:
    PhotonSpectrumSelection(): GeneralPhotonSelection() {}
    PhotonSpectrumSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t cpv = 10., Float_t disp = 3.0, Float_t t = 999):
        GeneralPhotonSelection(name, title, ec, a, n),
        fDistanceCPV(cpv),
        fDispersionCut(disp),
        fTimingCut(t)
    {}

    virtual void InitSelectionHistograms();

protected:
    virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);

    PhotonSpectrumSelection(const PhotonSpectrumSelection &);
    PhotonSpectrumSelection & operator = (const PhotonSpectrumSelection &);

    Float_t fDistanceCPV;
    Float_t fDispersionCut;
    Float_t fTimingCut;
private:
    ClassDef(PhotonSpectrumSelection, 2)
};
#endif