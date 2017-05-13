#ifndef PHYSMCPHOTONSELECTION_H
#define PHYSMCPHOTONSELECTION_H

// --- Custom header files ---
#include "PhysPhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class PhysMCPhotonSelection : public PhysPhotonSelection
{
public:
	PhysMCPhotonSelection(): PhysPhotonSelection() {}
	PhysMCPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, 
						 Int_t n = 3, Float_t t = 999, Float_t nona = 0., Float_t nonsigma = 1.): 
		PhysPhotonSelection(name, title, ec, a, n, t),
		fNonA(nona),
		fNonSigma(nonsigma) 
	{}

protected:
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual Float_t Nonlinearity(Float_t x) const;

	PhysMCPhotonSelection(const PhysMCPhotonSelection &);
	PhysMCPhotonSelection & operator = (const PhysMCPhotonSelection &);

	// Parameters of nonlinearity parametrization
	Float_t fNonA;
	Float_t fNonSigma;

private:
	ClassDef(PhysMCPhotonSelection, 2)
};
#endif