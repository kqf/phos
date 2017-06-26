#ifndef PHYSPHOTONSELECTIONMC_H
#define PHYSPHOTONSELECTIONMC_H

// --- Custom header files ---
#include "PhysPhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class PhysPhotonSelectionMC : public PhysPhotonSelection
{
public:
	PhysPhotonSelectionMC(): PhysPhotonSelection() {}
	PhysPhotonSelectionMC(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0,
	                      Int_t n = 3, Float_t t = 999, Float_t nona = 0., Float_t nonsigma = 1., Float_t genergy = 1.):
		PhysPhotonSelection(name, title, ec, a, n, t),
		fNonA(nona),
		fNonSigma(nonsigma),
		fGlobalEnergyScale(genergy)
	{}

protected:
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual Float_t Nonlinearity(Float_t x) const;

	PhysPhotonSelectionMC(const PhysPhotonSelectionMC &);
	PhysPhotonSelectionMC & operator = (const PhysPhotonSelectionMC &);

	// Parameters of nonlinearity parametrization
	Float_t fNonA;
	Float_t fNonSigma;
	Float_t fGlobalEnergyScale;

private:
	ClassDef(PhysPhotonSelectionMC, 2)
};
#endif