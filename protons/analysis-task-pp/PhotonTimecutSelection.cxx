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
	return TMath::Abs(clus->GetTOF()) < fTimingCut;
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
		fListOfHistos->Add(new TH2F(Form("h%sMassPtN3", suff), "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainMain", suff), "(M,p_{T})_{#gamma#gamma}, main-main; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtMainPileup", suff), "(M,p_{T})_{#gamma#gamma}, main-pileup; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("h%sMassPtPileupPileup", suff), "(M,p_{T})_{#gamma#gamma}, pileup-pileup; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	}

	// Use these histograms for analysis
	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
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

	// Apply assymetry cut
	Double_t asym = TMath::Abs( (p1.E() - p2.E()) / (p1.E() + p2.E()) );
	if(asym > fAsymmetryCut) return;

	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	const char * suff = eflags.isMixing ? "Mix" : "";
	FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12);

	Bool_t bc1 = IsMainBC(c1);
	Bool_t bc2 = IsMainBC(c2);

	if (bc1 && bc1)
		FillHistogram(Form("h%sMassPtMainMain", suff), ma12, pt12);

	if (bc1 ^ bc2)
		FillHistogram(Form("h%sMassPtMainPileup", suff), ma12, pt12);

	if ((!bc1) && (!bc2))
		FillHistogram(Form("h%sMassPtPileupPileup", suff), ma12, pt12);
}