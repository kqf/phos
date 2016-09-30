#include "PhotonSelection.h"

ClassImp(PhotonSelection);

//________________________________________________________________
void PhotonSelection::FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags)
{
	// Ensure that we are not doing mixing
	EventFlags flags = eflags;
	flags.isMixing = kFALSE;

	// Select photons
	TObjArray photonCandidates;
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
void PhotonSelection::MixPhotons(TObjArray & photonCandidates, TList * pool, const EventFlags & eflags)
{
	// Notify all selections that this is mixing
	EventFlags mflags = eflags;
	mflags.isMixing = kTRUE;

	// Apply user selection
	TObjArray previousPhotons;
	for (Int_t ev = 0; ev < pool->GetEntries(); ++ev)
	{
		TObjArray * previousClusters = dynamic_cast<TObjArray *>(pool->At(ev));
		if (!previousClusters) continue;
		SelectPhotonCandidates(previousClusters, &previousPhotons, mflags);
	}

	// Check all possible combinations
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); ++i)
	{
		AliVCluster * clus1 = (AliVCluster *) photonCandidates.At(i);

		// old cluster loop
		for (Int_t j = 0; j < previousPhotons.GetEntriesFast(); ++j)
		{
			AliVCluster * clus2 = (AliVCluster *) previousPhotons.At(j);
			ConsiderPair(clus1, clus2, mflags);
		} // old cluster loop
	}
}

//________________________________________________________________
Int_t PhotonSelection::CheckClusterGetSM(const AliVCluster * clus) const
{
	// Apply common cluster cuts and return supermodule number on success.
	// Return -1 if cuts not passed or an error occured.

	if (!clus->IsPHOS()) return -1;
	if (clus->GetType() != AliVCluster::kPHOSNeutral) return -1; // don't use CPV
	if (clus->GetNCells() < 1) return -1;

	Int_t sm = 1 + (clus->GetCellAbsId(0) - 1) / 3584;

	// check for data corruption to avoid segfaults
	if (sm < 1 || sm > 5)
	{
		AliError("Data corrupted");
		return -1;
	}
	return sm;
}