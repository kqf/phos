// --- Custom header files ---
#include "NonlinearityScanSelection.h"

// --- AliRoot header files ---
#include <AliPHOSAodCluster.h>
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(NonlinearityScanSelection);


//________________________________________________________________
TLorentzVector NonlinearityScanSelection::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
	Float_t energy = c1->E();

	TLorentzVector p;
	c1->GetMomentum(p, eflags.vtxBest);
	p *= Nonlinearity(energy);
	return p;
}

//________________________________________________________________
Float_t NonlinearityScanSelection::Nonlinearity(Float_t x) const
{
	return fGlobalEnergyScale * (1. + fNonA * TMath::Exp(-x / 2. * x / fNonSigma / fNonSigma));
}

//________________________________________________________________
void NonlinearityScanSelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 20;

	for (Int_t i = 0; i < 2; ++i)
	{
		const char * s = (i == 0) ? "" : "Mix";
		TH1 * hist = new TH2F(Form("h%sMassPt", s), "(M,p_{T})_{#gamma#gamma}, ; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
		fInvariantMass[i] = new DetectorHistogram(hist, fListOfHistos);
	}

	//for non-linearity study
	const Int_t Na = 7;
	const Int_t Nb = 7;

	for (Int_t ia = 0; ia < Na; ia++)
	{
		for (Int_t ib = 0; ib < Nb; ib++)
		{
			Double_t a = -0.07 + 0.01 * ia; //change scaned area, depending of your parameter
			Double_t b =  0.4  + 0.1 * ib; //change scaned area, depending of your parameter

			for (Int_t i = 0; i < 2; ++i)
			{
				const char * s = (i == 0) ? "" : "Mix";
				fListOfHistos->Add(new TH2F(Form("h%sMassPt_%d_%d", s, ia, ib), "(M,p_{T})_{#gamma#gamma}, ; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
			}
		}
	}


	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

// These histograms are needed only to check the performance
// Don't do any analysis with these histograms.
//

	fClusters = new TH1F("hClusterPt_SM0", "Cluster p_{T} spectrum with default cuts, all modules; p_{T}, GeV/c", nPt, ptMin, ptMax);
	fListOfHistos->Add(fClusters);
}


void InitSelectionHistograms::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok
	const char * s = eflags.isMixig ? "Mix" : "";

	for (Int_t ia = 0; ia < 7; ia++)
	{
		for (Int_t ib = 0; ib < 7; ib++)
		{
			// TODO: Override this behaviour
			TLorentzVector p1 = ClusterMomentum(c1, eflags, ia, ib);
			TLorentzVector p2 = ClusterMomentum(c2, eflags, ia, ib);
			TLorentzVector psum = p1 + p2;

			// Pair cuts can be applied here
			if (psum.M2() < 0)  return;


			Double_t ma12 = psum.M();
			Double_t pt12 = psum.Pt();
			FillHistogram("h%sMassPt_%d_%d", s, ia, ib), m12, pt12);
		}
	}
}

