#ifndef QUALITYSELECTION_H
#define QUALITYSELECTION_H

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class PhotonSpectrumSelection : public GeneralPhotonSelection
{
public:
    PhotonSpectrumSelection(): GeneralPhotonSelection() {}
    PhotonSpectrumSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999, Float_t cpv = 10., Float_t disp = 3.0):
        GeneralPhotonSelection(name, title, ec, a, n, t),
        fDistanceCPV(cpv),
        fDispersionCut(disp)
    {}

    virtual void InitSelectionHistograms();

    // There is no need to mix events 
    virtual void MixPhotons(TClonesArray & photons, TList * pool, const EventFlags & eflags)
    {
        (void) photons;
        (void) pool;
        (void) eflags;
    }
    
protected:
    virtual void FillClusterHistograms(const AliVCluster * c, const EventFlags & eflags);

    PhotonSpectrumSelection(const PhotonSpectrumSelection &);
    PhotonSpectrumSelection & operator = (const PhotonSpectrumSelection &);

    Float_t fDistanceCPV;
    Float_t fDispersionCut;
private:
    ClassDef(PhotonSpectrumSelection, 2)
};
#endif