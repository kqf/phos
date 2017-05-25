// --- Custom header files ---
#include "PhysMCPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---

// --- AliRoot header files ---
#include <AliPHOSAodCluster.h>
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(PhysMCPhotonSelection);


//________________________________________________________________
TLorentzVector PhysMCPhotonSelection::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
    // TODO: Check if this is a proper procedure
    Float_t energy = c1->E();

    TLorentzVector p;
    c1->GetMomentum(p, eflags.vtxBest);
    p *= Nonlinearity(energy);
	return p;
}

//________________________________________________________________
Float_t PhysMCPhotonSelection::Nonlinearity(Float_t x) const
{
    // TODO: Find out what to do with global energy scale
    Float_t gloabl_energy_scale = 1.04;
	return gloabl_energy_scale * (1. + fNonA * TMath::Exp(-x / 2. * x / fNonSigma / fNonSigma));
}


