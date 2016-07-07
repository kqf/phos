#include "PhotonSelection.h"


ClassImp(PhotonSelection);

//________________________________________________________________
void PhotonSelection::FillPi0Mass(TObjArray * clusArray, const EventFlags & eflags)
{
	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, eflags);

	// All possible combinations on photon candadates
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); i++)
	{
		AliVCluster * clus1 = (AliVCluster *) photonCandidates.At(i);

		// second cluster loop
		for (Int_t j = i + 1; j < photonCandidates.GetEntriesFast(); j++)
		{
			AliVCluster * clus2 = (AliVCluster *) photonCandidates.At(j);
			ConsiderPair(clus1, clus2, eflags);
		} // second cluster loop
	} // cluster loop
}

//________________________________________________________________
Int_t PhotonSelection::CheckClusterGetSM(const AliVCluster * clus) const
{
	// Apply common cluster cuts and return supermodule number on success.
	// Return -1 if cuts not passed or an error occured.

	if (!clus->IsPHOS()) return -1;
	if (clus->GetNCells() < 1) return -1;

	Int_t sm = 1 + (clus->GetCellAbsId(0) - 1) / 3584;

	// check for data corruption to avoid segfaults
	if (sm < 0 || sm > 9)
	{
		AliError("Data corrupted");
		return -1;
	}
	return sm;
}