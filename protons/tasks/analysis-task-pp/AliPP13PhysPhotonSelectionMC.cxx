// --- Custom header files ---
#include "AliPP13PhysPhotonSelectionMC.h"

// --- AliRoot header files ---
#include <AliPHOSAodCluster.h>
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(AliPP13PhysPhotonSelectionMC);


//________________________________________________________________
TLorentzVector AliPP13PhysPhotonSelectionMC::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
    Float_t energy = c1->E();

    TLorentzVector p;
    c1->GetMomentum(p, eflags.vtxBest);
    p *= fWeights->Nonlinearity(energy);
	return p;
}

//________________________________________________________________
Bool_t AliPP13PhysPhotonSelectionMC::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
}

