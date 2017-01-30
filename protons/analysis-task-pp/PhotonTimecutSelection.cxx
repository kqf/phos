// --- Custom header files ---
#include "PhotonTimecutSelection.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>
// #include "THashList.h"

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
	// Float_t timesigma = 23.e-9; // 23 ns
	// Timecut from histogram scaled by energy
	// Timecut according to resolution
	Float_t timesigma = 12.5e-9; // 50 ns
	if (TMath::Abs(clus->GetTOF()) < timesigma) return kTRUE;
	return kFALSE;
}

//________________________________________________________________
void PhotonTimecutSelection::InitSelectionHistograms()
{

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
		fListOfHistos->Add(new TH3F(Form("h%sMassPtTOF", suff), "(M,p_{T})_{#gamma#gamma}, main-main; M_{#gamma#gamma}, GeV; p_{T}, GeV/c; tof, s", nM, mMin, mMax, nPt, ptMin, ptMax, 50, 0, 0.05 * 1e-6));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainMain", suff), "(M,p_{T})_{#gamma#gamma}, main-main; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainPileup", suff), "(M,p_{T})_{#gamma#gamma}, main-pileup; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtPileupPileup", suff), "(M,p_{T})_{#gamma#gamma}, pileup-pileup; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	}

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterTime%d", i), mtitle("Cluster Time scaled by E, %s; t, s", i), 4800, -0.25 * 1e-6, 0.25 * 1e-6));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hClusterEvsTM%d", i), mtitle("Cluster energy vs time, %s; cluster energy, GeV; time, s", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hClusterTimeMap%d", i), mtitle("Cluster time map, %s; X; Z", i), 64, 0.5, 64.5, 56, 0.5, 56.5));

}

//________________________________________________________________
void PhotonTimecutSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

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

	Float_t tof1 = TMath::Abs(c1->GetTOF());
	Float_t tof2 = TMath::Abs(c2->GetTOF());
	FillHistogram(Form("h%sMassPtTOF", suff), ma12, pt12, TMath::Max(tof1, tof2));

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
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->GetNCells() < fNCellsCut) continue;
		if (clus->E() < fClusterMinE) continue;
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
		FillHistogram(Form("hClusterTimeMap%d", sm), x, z, tof);


		FillHistogram(Form("hClusterTime%d", 0), tof, clus->E());
		FillHistogram(Form("hClusterEvsTM%d", 0), clus->E(), tof);
		FillHistogram(Form("hClusterTimeMap%d", 0), x, z, tof);
	}

}