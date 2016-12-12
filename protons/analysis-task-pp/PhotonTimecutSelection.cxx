// --- Custom header files ---
#include "PhotonTimecutSelection.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>
#include <AliPHOSGeometry.h>

#include <iostream>
using namespace std;

ClassImp(PhotonTimecutSelection);


Bool_t PhotonTimecutSelection::IsMainBC(const AliVCluster * clus) const
{
	// The value obtained from the fit

	// It's unknown if I should implement symmetric cut or not.
	Float_t timesigma = 23.e-9; // 23 ns

	if (TMath::Abs(clus->GetTOF()) < 3 * timesigma) return kTRUE;
	return kFALSE;
}

//________________________________________________________________
void PhotonTimecutSelection::InitSummaryHistograms()
{
	if (fListOfHistos)
		AliFatal("Trying to reinitialize list of histograms");

	fListOfHistos = new TList();
	fListOfHistos->SetOwner(kTRUE);

	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 500;
	Double_t ptMin = 0;
	Double_t ptMax = 100;

	for (Int_t i = 0; i < 2; i++)
	{
		const char * suff = (i == 0) ? "" : "Mix";
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainMain", suff), "(M,p_{T})_{#gamma#gamma}, main-main", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainPileup", suff), "(M,p_{T})_{#gamma#gamma}, main-pileup", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtPileupPileup", suff), "(M,p_{T})_{#gamma#gamma}, pileup-pileup", nM, mMin, mMax, nPt, ptMin, ptMax));
	}

	for (Int_t i = 0; i < 5;  ++i)
	{
		fListOfHistos->Add(new TH1F(Form("hClusterTime%d", i), Form("Cluster Time scaled by E, M%d", i), 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("hClusterEvsTM%d", i), Form("Cluster energy vs time, M%d", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("hClusterPtvsTM%d", i), Form("Cluster Pt vs time, M%d", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("hClusterXvsTM%d", i), Form("Cluster X vs time, M%d", i),  64, 0.5, 64.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("hClusterZvsTM%d", i), Form("Cluster Z vs time, M%d", i),  56, 0.5, 56.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("hClusterTimeMap%d", i), Form("Cluster time map, M%d", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
		fListOfHistos->Add(new TH2F(Form("hClusterNvsTM%d", i), Form("Cluster energy vs time, M%d", i), 25, 0.5, 25.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
	}
}

//________________________________________________________________
void PhotonTimecutSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

	// Only physical clusters
	if (c1->GetNCells() < 3 || c2->GetNCells() < 3) return;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;
	// if (psum.Pt() < 2.) return;

	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	const char * suff = eflags.isMixing ? "Mix" : "";
	Bool_t bc1 = IsMainBC(c1);
	Bool_t bc2 = IsMainBC(c2);

	if (bc1 && bc1)
		FillHistogram(Form("h%sMassPtMainMain", suff), ma12, pt12);

	if (bc1 ^ bc2)
		FillHistogram(Form("h%sMassPtMainPileup", suff), ma12, pt12);

	if ((!bc1) && (!bc2))
		FillHistogram(Form("h%sMassPtPileupPileup", suff), ma12, pt12);
}

//________________________________________________________________
void PhotonTimecutSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Double_t pi0EClusMin = 0.3;
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->GetNCells() < 3) continue;
		if (clus->E() < pi0EClusMin) continue;
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		candidates->Add(clus);

		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;
		TLorentzVector p;
		clus->GetMomentum(p, eflags.vtxBest);

		Float_t tof = clus->GetTOF();
		FillHistogram(Form("hClusterTime%d", sm), tof, clus->E());

		FillHistogram(Form("hClusterEvsTM%d", sm), clus->E(), tof);
		FillHistogram(Form("hClusterPtvsTM%d", sm), p.Pt(), tof);
		FillHistogram(Form("hClusterXvsTM%d", sm), x, tof);
		FillHistogram(Form("hClusterZvsTM%d", sm), z, tof);
		FillHistogram(Form("hClusterTimeMap%d", sm), x, z, tof);
		FillHistogram(Form("hClusterNvsTM%d", sm), clus->GetNCells(), tof);


		FillHistogram(Form("hClusterTime%d", 0), tof, clus->E());

		FillHistogram(Form("hClusterEvsTM%d", 0), clus->E(), tof);
		FillHistogram(Form("hClusterPtvsTM%d", 0), p.Pt(), tof);
		FillHistogram(Form("hClusterXvsTM%d", 0), x, tof);
		FillHistogram(Form("hClusterZvsTM%d", 0), z, tof);
		FillHistogram(Form("hClusterTimeMap%d", 0), x, z, tof);
		FillHistogram(Form("hClusterNvsTM%d", 0), clus->GetNCells(), tof);

	}

}