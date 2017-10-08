#ifndef ALIPP13WEIGHEDPHYSPHOTONSELECTIONMC_H
#define ALIPP13WEIGHEDPHYSPHOTONSELECTIONMC_H

// --- Custom header files ---
#include "AliPP13PhysPhotonSelectionMC.h"

// --- AliRoot header files ---
#include <AliVCluster.h>

class AliPP13WeighedPhysPhotonSelectionMC : public AliPP13PhysPhotonSelectionMC
{
public:
	AliPP13WeighedPhysPhotonSelectionMC(): AliPP13PhysPhotonSelectionMC() {}
	AliPP13WeighedPhysPhotonSelectionMC(const char * name, const char * title, AliPP13ClusterCuts cuts, 
				Float_t nona = 0., Float_t nonsigma = 1., Float_t genergy = 1.,
				Float_t wa = 0., Float_t wsigma = 1., Float_t wscale = 1.):
		AliPP13PhysPhotonSelectionMC(name, title, cuts, nona, nonsigma, genergy),
		fWeighA(wa),
		fWeighSigma(wsigma),
		fWeighScale(wscale)
	{
		fCuts.fTimingCut = 99999; // No timing cut in MC
	}

protected:
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual Float_t Weigh(Float_t x) const;

	AliPP13WeighedPhysPhotonSelectionMC(const AliPP13WeighedPhysPhotonSelectionMC &);
	AliPP13WeighedPhysPhotonSelectionMC & operator = (const AliPP13WeighedPhysPhotonSelectionMC &);

	// Parameters of weighed MC parametrization
	Float_t fWeighA;
	Float_t fWeighSigma;
	Float_t fWeighScale;

private:
	ClassDef(AliPP13WeighedPhysPhotonSelectionMC, 2)
};
#endif