// --- Custom header files ---
#include "QualityPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliPHOSGeometry.h>

#include <iostream>
using namespace std;


ClassImp(QualityPhotonSelection);

//________________________________________________________________
void QualityPhotonSelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 500;
	Double_t ptMin = 0;
	Double_t ptMax = 100;


	// Info about selected clusters
	fListOfHistos->Add(new TH2F("hNcellsE", "Cell multiplicity; E, GeV; N_{cell}", 41, 0, 40, 81, 0, 80));
	fListOfHistos->Add(new TH2F("hShapeE", "Cluster shape; E, GeV; M20, cm", 41, 0, 40, 41, 0, 40));


	// Heatmap check for physics
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluNXZM_0_SM%d", i), mtitle("Cluster N(X,Z), %s, E < 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluEXZM_0_SM%d", i), mtitle("Cluster E(X,Z), %s, E < 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluNXZM_1_SM%d", i), mtitle("Cluster N(X,Z), %s, E > 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluEXZM_1_SM%d", i), mtitle("Cluster E(X,Z), %s, E > 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));



	// Heatmap check for physics + check abs Id numbering
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_0_SM%d", i), mtitle("Cluster N(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_0_SM%d", i), mtitle("Cluster E(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_1_SM%d", i), mtitle("Cluster N(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_1_SM%d", i), mtitle("Cluster E(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	
	// Test Assymetry cut
	//
	fListOfHistos->Add(new TH3F("hMassPtN3A", "(M,p_{T}, A)_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax, 20, 0., 1.));
	fListOfHistos->Add(new TH3F("hMixMassPtN3A", "(M,p_{T}, A)_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax, 20, 0., 1.));

	fListOfHistos->Add(new TH2F("hAsymmetry", "(p_{T}, A)_{#gamma#gamma}, N_{cell}>2; p_{T}, GeV/c, Asymmetry ", nPt, ptMin, ptMax / 2., 20, 0., 1.));
	fListOfHistos->Add(new TH2F("hMixAsymmetry", "(p_{T}, A)_{#gamma#gamma}, N_{cell}>2; p_{T}, GeV/c, Asymmetry ", nPt, ptMin, ptMax / 2., 20, 0., 1.));


	// Timing cut
	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterTime%d", i), mtitle("Cluster Time scaled by E, %s; t, s", i), 4800, -0.25 * 1e-6, 0.25 * 1e-6));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hClusterEvsTM%d", i), mtitle("Cluster energy vs time, %s; cluster energy, GeV; time, s", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hClusterTimeMap%d", i), mtitle("Cluster time map, %s; X; Z", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
}


//________________________________________________________________
void QualityPhotonSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;

	// Appply asymmetry cut for pair
	Double_t asym = TMath::Abs( (p1.E() - p2.E()) / (p1.E() + p2.E()) );
	if (asym > fAsymmetryCut) return;


	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	const char * suff = eflags.isMixing ? "Mix" : "";
	FillHistogram(Form("h%sMassPtN3A", suff), ma12 , pt12, asym);
	FillHistogram(Form("h%sAsymmetry", suff), pt12, asym);
}


//________________________________________________________________
void QualityPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
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

		Float_t tof = clus->GetTOF();

		if (!eflags.isMixing)
		{
			FillHistogram(Form("hClusterTime%d", sm), tof, clus->E());
			FillHistogram(Form("hClusterEvsTM%d", sm), clus->E(), tof);
			FillHistogram(Form("hClusterTimeMap%d", sm), x, z, tof);

			FillHistogram(Form("hClusterTime%d", 0), tof, clus->E());
			FillHistogram(Form("hClusterEvsTM%d", 0), clus->E(), tof);
			FillHistogram(Form("hClusterTimeMap%d", 0), x, z, tof);

		}
		if (TMath::Abs(clus->GetTOF()) > fTimingCut) continue;

		if (!eflags.isMixing) FillHistogram("hNcellsE", p.E(), clus->GetNCells());
		if (!eflags.isMixing) FillHistogram("hShapeE", clus->GetM20(), clus->GetNCells());

		if (clus->GetNCells() < fNCellsCut) continue;
		candidates->Add(clus);


		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;
		
		Float_t energy = clus->E();
		Int_t isHighECluster = Int_t(energy > 1.);

		FillHistogram(Form("hCluNXZM_%d_SM%d", isHighECluster, sm), x, z, 1.);
		FillHistogram(Form("hCluEXZM_%d_SM%d", isHighECluster, sm), x, z, energy);

		FillHistogram(Form("hClusterIdN_%d_SM%d", isHighECluster, sm), AbsId(x, z, sm));
		FillHistogram(Form("hClusterIdE_%d_SM%d", isHighECluster, sm), AbsId(x, z, sm), energy);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		FillHistogram("EventCounter", 2.5);
}

// Default version defined in PHOSutils uses ideal geometry
// use this instead
Int_t QualityPhotonSelection::AbsId(Int_t x, Int_t z, Int_t sm) const
{
	// Converts cell absId --> (sm,eta,phi);
	AliPHOSGeometry * geomPHOS = AliPHOSGeometry::GetInstance("Run2");

	if (!geomPHOS)
		AliFatal("Geometry is not defined");

	for (Int_t id = (3584 * (sm - 1) + 1); id <= (3584 * (sm)); ++id)
	{
		Int_t rel[4];
		geomPHOS->AbsToRelNumbering(id, rel);

		if (rel[2] == x && rel[3] == z)
			return id;
	}

	// There is no such a cell
	return -1;
}