// --- Custom header files ---
#include "AliPP13WeighedPhysPhotonSelectionMC.h"

// --- AliRoot header files ---
#include <AliPHOSAodCluster.h>
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(AliPP13WeighedPhysPhotonSelectionMC);


//________________________________________________________________
TLorentzVector AliPP13WeighedPhysPhotonSelectionMC::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
    TLorentzVector p = AliPP13PhysPhotonSelectionMC::ClusterMomentum(c1, eflags);
    p *= Weigh(energy);
	return p;
}

//________________________________________________________________
Float_t AliPP13WeighedPhysPhotonSelectionMC::Weigh(Float_t x) const
{
	return fWeighScale * (1. + fWeighA * TMath::Exp(-x / 2. * x / fWeighSigma / fWeighSigma));
}


