// --- Custom header files ---
#include "PhysPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(PhysPhotonSelection);


//________________________________________________________________
void PhysPhotonSelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 500;
	Double_t ptMin = 0;
	Double_t ptMax = 100;

	fListOfHistos->Add(new TH2F("hMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));

	fListOfHistos->Add(new TH3F("hMassPtN3A", "(M,p_{T}, A)_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax, 20, 0., 1.));
	fListOfHistos->Add(new TH3F("hMixMassPtN3A", "(M,p_{T}, A)_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax, 20, 0., 1.));

	fListOfHistos->Add(new TH2F("hAsymmetry", "(p_{T}, A)_{#gamma#gamma}, N_{cell}>2; p_{T}, GeV/c, Asymmetry ", nPt, ptMin, ptMax / 2., 20, 0., 1.));
	fListOfHistos->Add(new TH2F("hMixAsymmetry","(p_{T}, A)_{#gamma#gamma}, N_{cell}>2; p_{T}, GeV/c, Asymmetry ", nPt, ptMin, ptMax / 2., 20, 0., 1.));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_SM%d", i), mtitle("Cluster p_{T} spectrum, %s; p_{T}, GeV/c", i), nPt, ptMin, ptMax));

	// TODO: fix this for CAF
	Int_t kMinModule = 1;
	Int_t kMaxModule = 4;

	// Different modules histograms
	for (Int_t sm = kMinModule; sm < (kMaxModule + 1); sm++)
		for (Int_t sm2 = sm; sm2 < (kMaxModule + 1); sm2++)
			fListOfHistos->Add(new TH2F(Form("hMassPtSM%dSM%d", sm, sm2), "(M,p_{T})_{#gamma#gamma}; m_{#gamma #gamma}, GeV/c^{2} ; p_{T}, GeV/c"  , nM, mMin, mMax, nPt, ptMin, ptMax));

	for (Int_t sm = kMinModule; sm < (kMaxModule + 1); sm++)
		for (Int_t sm2 = sm; sm2 < (kMaxModule + 1); sm2++)
			fListOfHistos->Add(new TH2F(Form("hMixMassPtSM%dSM%d", sm, sm2), "(M,p_{T})_{#gamma#gamma}; m_{#gamma #gamma}, GeV/c^{2} ; p_{T}, GeV/c"  , nM, mMin, mMax, nPt, ptMin, ptMax));	

	for(Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if(!hist) continue;
		hist->Sumw2();
	}
}

//________________________________________________________________
void PhysPhotonSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;
	// if (psum.Pt() < 2.) return;

	Double_t asym = TMath::Abs( (p1.E() - p2.E()) / (p1.E() + p2.E()) );

	// Appply asymmetry cut for pair
	if(asym > fAsymmetryCut) return;

	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	if (pt12 < 1) return;

	const char * suff = eflags.isMixing ? "Mix" : "";
	FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12);

	FillHistogram(Form("h%sMassPtN3A", suff), ma12 , pt12, asym);

	// TODO: move asymmetry plots to Quality section
	FillHistogram(Form("h%sAsymmetry", suff), pt12, asym);


	if (sm1 < sm2)
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm1, sm2), ma12, pt12);
	else
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm2, sm1), ma12, pt12);
}

//________________________________________________________________
void PhysPhotonSelection::FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags)
{
	TLorentzVector p;
	clus->GetMomentum(p, eflags.vtxBest);	
	FillHistogram(Form("hClusterPt_SM%d", 0), p.Pt());
}