// --- Custom header files ---
#include "PhysMCPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---

// --- AliRoot header files ---
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(PhysMCPhotonSelection);


//________________________________________________________________
TLorentzVector PhysMCPhotonSelection::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
	TLorentzVector p;
	c1->GetMomentum(p, eflags.vtxBest);
    // TODO: Check if this is a proper procedure
	// Float_t energy  = p.E();
	// p.SetE(energy * Nonlinearity(energy));
	return p;
}

//________________________________________________________________
Float_t PhysMCPhotonSelection::Nonlinearity(Float_t x) const
{
	return 1.00 * (1. + fNonA * TMath::Exp(-x / 2 * x / 2 / 2. / fNonSigma / fNonSigma));
}


