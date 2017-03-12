// --- Custom header files ---
#include "TagAndProbeSelection.h"

// --- ROOT system ---
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(TagAndProbeSelection);


//________________________________________________________________
void TagAndProbeSelection::FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags)
{
	(void) pool;
	// Ensure that we are not doing mixing
	EventFlags flags = eflags;
	flags.isMixing = kFALSE;

	// Select photons
	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);

	// Consider N^2 - N combinations, excluding only same-same clusters.
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); i++)
	{
		AliVCluster * tag = dynamic_cast<AliVCluster *> (photonCandidates.At(i));

		if (TMath::Abs(tag->GetTOF()) > fTimingCut)
			continue;

		for (Int_t j = 0; j < photonCandidates.GetEntriesFast(); j++)
		{
			if(i == j) // Skip the same clusters
				continue;

			AliVCluster * proble = dynamic_cast<AliVCluster *> (photonCandidates.At(j));
			ConsiderPair(tag, proble, flags);
		} // second cluster loop
	} // cluster loop

	MixPhotons(photonCandidates, pool, flags);
}

//________________________________________________________________
void TagAndProbeSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
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

	const char * suff = eflags.isMixing ? "Mix" : "";

	FillHistogram(Form("h%sMassEnergyAll_SM%d", suff, 0), m12 , energy);

	if(sm1 == sm2)
		FillHistogram(Form("h%sMassEnergyAll_SM%d", suff, sm1), m12 , energy);

	if (TMath::Abs(c2->GetTOF()) > fTimingCut)
		return;

	FillHistogram(Form("h%sMassEnergyTOF_SM%d", suff, 0), m12 , energy);

	if(sm1 == sm2)
		FillHistogram(Form("h%sMassEnergyTOF_SM%d", suff, sm1), m12 , energy);
}


//________________________________________________________________
void TagAndProbeSelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 250;
	Double_t mMin  = 0.0;
	Double_t mMax  = 0.3;

	Int_t nE      = 400;
	Double_t eMin = 0;
	Double_t eMax = 20;


	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hMassEnergyAll_SM%d", i), mtitle("(M_{#gamma#gamma}, E_{probe}); M_{#gamma#gamma}, GeV; E_{proble}, GeV", i), nM, mMin, mMax, nE, eMin, eMax));	

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hMassEnergyTOF_SM%d", i), mtitle("(M_{#gamma#gamma}, E_{probe}); M_{#gamma#gamma}, GeV; E_{proble}, GeV", i), nM, mMin, mMax, nE, eMin, eMax));	

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hMixMassEnergyAll_SM%d", i), mtitle("(M_{#gamma#gamma}, E_{probe}); M_{#gamma#gamma}, GeV; E_{proble}, GeV", i), nM, mMin, mMax, nE, eMin, eMax));	

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hMixMassEnergyTOF_SM%d", i), mtitle("(M_{#gamma#gamma}, E_{probe}); M_{#gamma#gamma}, GeV; E_{proble}, GeV", i), nM, mMin, mMax, nE, eMin, eMax));	


	for(Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if(!hist) continue;
		hist->Sumw2();
	}

}


//________________________________________________________________
void TagAndProbeSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		TLorentzVector p;
		clus->GetMomentum(p, eflags.vtxBest);

		if (clus->E() < fClusterMinE) continue;
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		if (clus->GetNCells() < fNCellsCut) continue;
		// Don't cut on variables we want to study:
		// In this case it's TOF

		candidates->Add(clus);

		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;

		if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
			FillHistogram("EventCounter", 2.5);
	}
}