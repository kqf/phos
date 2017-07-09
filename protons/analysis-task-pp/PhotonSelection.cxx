// --- Custom header files ---
#include "PhotonSelection.h"

// --- AliRoot header files ---
#include "AliPHOSGeometry.h"


ClassImp(PhotonSelection);

//________________________________________________________________
void PhotonSelection::FillPi0Mass(TClonesArray * clusArray, TList * pool, const EventFlags & eflags)
{
	// Ensure that we are not doing mixing
	EventFlags flags = eflags;
	flags.isMixing = kFALSE;

	// Select photons
	TClonesArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);

	// All possible combinations on photon candadates
	// Int_t counter = 0;
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); i++)
	{
		AliVCluster * clus1 = (AliVCluster *) photonCandidates.At(i);

		// second cluster loop
		for (Int_t j = i + 1; j < photonCandidates.GetEntriesFast(); j++)
		{
			// ++counter;
			AliVCluster * clus2 = (AliVCluster *) photonCandidates.At(j);
			ConsiderPair(clus1, clus2, flags);
		} // second cluster loop
	} // cluster loop

	// Int_t Nn = photonCandidates.GetEntriesFast();
	// std::cout << "Number of combinations: " << counter << " should be " << Nn * (Nn - 1.) / 2. << std::endl;

	MixPhotons(photonCandidates, pool, flags);
}

//________________________________________________________________
void PhotonSelection::MixPhotons(TClonesArray & photonCandidates, TList * pool, const EventFlags & eflags)
{
	// Notify all selections that this is mixing
	EventFlags mflags = eflags;
	mflags.isMixing = kTRUE;

	// Apply user selection
	TClonesArray previousPhotons;
	for (Int_t ev = 0; ev < pool->GetEntries(); ++ev)
	{
		TClonesArray * previousClusters = dynamic_cast<TClonesArray *>(pool->At(ev));
		if (!previousClusters) continue;
		SelectPhotonCandidates(previousClusters, &previousPhotons, mflags);
	}

	// old cluster loop
	for (Int_t j = 0; j < previousPhotons.GetEntriesFast(); ++j)
	{
		AliVCluster * clus1 = (AliVCluster *) previousPhotons.At(j);

		// Check all possible combinations
		for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); ++i)
		{
			AliVCluster * clus2 = (AliVCluster *) photonCandidates.At(i);
			ConsiderPair(clus1, clus2, mflags);
		}
	} // old cluster loop
}

//________________________________________________________________
Int_t PhotonSelection::CheckClusterGetSM(const AliVCluster * clus, Int_t & x, Int_t & z) const
{
	// Apply common cluster cuts and return supermodule number on success.
	// Return -1 if cuts not passed or an error occured.

	if (!clus->IsPHOS()) return -1;
	if (clus->GetType() != AliVCluster::kPHOSNeutral) return -1; // don't use CPV
	if (clus->GetNCells() < 1) return -1;

	Float_t  position[3];
	clus->GetPosition(position);
	TVector3 global(position);

	Int_t relId[4];
	AliPHOSGeometry * phosGeometry = AliPHOSGeometry::GetInstance();
	// AliPHOSGeometry * phosGeometry = AliPHOSGeometry::GetInstance("IHEP");
	// AliPHOSGeometry * phosGeometry = AliPHOSGeometry::GetInstance("Run2") ;
	phosGeometry->GlobalPos2RelId(global, relId) ;

	Int_t sm = relId[0];
	x = relId[2];
	z = relId[3];

	// check for data corruption to avoid segfaults
	if (sm < 1 || sm > 5)
	{
		AliError("Data is corrupted!!!");
		return -1;
	}

	return sm;
}

//________________________________________________________________
TLorentzVector PhotonSelection::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
	TLorentzVector p;
	c1->GetMomentum(p, eflags.vtxBest);		
	return p;
}
