// --- Custom header files ---
#include "AliPP13NonlinearitySelection.h"
#include "AliPP13DetectorHistogram.h"

// --- ROOT system ---
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(AliPP13NonlinearitySelection);


//________________________________________________________________
void AliPP13NonlinearitySelection::FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags)
{
	(void) pool;
	// Ensure that we are not doing mixing
	EventFlags flags = eflags;
	flags.isMixing = kFALSE;

	// Select photons
	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);

	// Consider N^2 - N combinations, excluding only same-same clusters.
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); ++i)
	{
		AliVCluster * first = dynamic_cast<AliVCluster *> (photonCandidates.At(i));

		for (Int_t j = 0; j < photonCandidates.GetEntriesFast(); ++j)
		{
			if (i == j) // Skip the same clusters
				continue;

			AliVCluster * second = dynamic_cast<AliVCluster *> (photonCandidates.At(j));
			ConsiderPair(first, second, flags);
		} // second cluster loop
	} // cluster loop

	MixPhotons(photonCandidates, pool, flags);
}

//________________________________________________________________
void AliPP13NonlinearitySelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;
	Float_t energy = p2.E();
	Float_t m12 = psum.M();


	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok

	Float_t weight = fWeights.Weight(energy);
	fMassEnergy[int(eflags.isMixing)]->FillAll(sm1, sm2, m12, energy, weight);
}


//________________________________________________________________
void AliPP13NonlinearitySelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 250;
	Double_t mMin  = 0.0;
	Double_t mMax  = 0.3;

	Int_t nE      = 2000;
	Double_t eMin = 0;
	Double_t eMax = 20;


	for (Int_t i = 0; i < 2; ++i)
	{
		const char * sf = (i == 0) ? "" : "Mix";
		TH2F * hist = new TH2F(Form("h%sMassEnergy_", sf), "(M_{#gamma#gamma}, E_{#gamma}) ; M_{#gamma#gamma}, GeV; E_{#gamma}, GeV", nM, mMin, mMax, nE, eMin, eMax);
		fMassEnergy[i] = new AliPP13DetectorHistogram(hist, fListOfHistos, AliPP13DetectorHistogram::kModules);
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

}