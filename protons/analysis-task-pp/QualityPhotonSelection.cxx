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
	Int_t nPt      = 500;
	Double_t ptMin = 0;
	Double_t ptMax = 100;


	// Info about selected clusters
	fListOfHistos->Add(new TH2F("hNcellsPt", "Cell multiplicity; N_{cell}; p_{T}, GeV/c" , 41, 0, 40, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hNcellsE", "Cell multiplicity; N_{cell}; E, GeV" , 41, 0, 40, nPt, ptMin, ptMax));

	// Heatmap check for physics
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluNXZM_0_SM%d", i), mtitle("Cluster N(X,Z), %s, E < 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluEXZM_0_SM%d", i), mtitle("Cluster E(X,Z), %s, E < 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluNXZM_1_SM%d", i), mtitle("Cluster N(X,Z), %s, E > 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH2F(Form("hCluEXZM_1_SM%d", i), mtitle("Cluster E(X,Z), %s, E > 1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));

	// Test physics selection in RUN2
	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterEnergy_SM%d", i), mtitle("Cluster energy, %s; cluster energy, GeV", i), 1000, 0., 100.));
	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hMainClusterEnergy_SM%d", i), mtitle("Cluster energy, %s; cluster energy, GeV", i), 1000, 0., 100.));

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

	// Heatmap check for physics + check abs Id numbering
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_0_SM%d", i), mtitle("Cluster N(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_0_SM%d", i), mtitle("Cluster E(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_1_SM%d", i), mtitle("Cluster N(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_1_SM%d", i), mtitle("Cluster E(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));

	// create histograms for L1 phase substraction test
	for (Int_t m = 5; m < 20; ++m)
		fListOfHistos->Add(new TH2F(Form("timeDLL%d", m), "Time, HG", 4, 0., 4., 200, -5.e-7, 5.e-7));
}

//________________________________________________________________
void QualityPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Double_t pi0EClusMin = 0.3;
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->E() < pi0EClusMin) continue;
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		candidates->Add(clus);


		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;
		TLorentzVector p;
		clus->GetMomentum(p, eflags.vtxBest);

		FillHistogram("hNcellsPt", clus->GetNCells(), p.Pt());
		FillHistogram("hNcellsE", clus->GetNCells(), p.E());

		FillHistogram(Form("hClusterEnergy_SM%d", 0), p.E());
		FillHistogram(Form("hClusterEnergy_SM%d", sm), p.E());

		Float_t energy = clus->E();
		Int_t isHighECluster = Int_t(energy > 1.);

		Float_t timesigma = 12.5e-9; // 12.5 ns
		if (TMath::Abs(clus->GetTOF()) > timesigma)
			continue;

		FillHistogram(Form("hMainClusterEnergy_SM%d", 0), p.E());
		FillHistogram(Form("hMainClusterEnergy_SM%d", sm), p.E());


		FillHistogram(Form("hCluNXZM_%d_SM%d", isHighECluster, sm), x, z, 1.);
		FillHistogram(Form("hCluEXZM_%d_SM%d", isHighECluster, sm), x, z, energy);

		FillHistogram(Form("hClusterIdN_%d_SM%d", isHighECluster, sm), AbsId(x, z, sm));
		FillHistogram(Form("hClusterIdE_%d_SM%d", isHighECluster, sm), AbsId(x, z, sm), energy);


		Int_t ddlID = WhichDDL(sm, x) ;
		Double_t time = clus->GetTOF() ;

		//
		// There should be some amplitude;
		//	   if (amplitude > 1.)

		if (p.E() > 1.)
			FillHistogram(Form("timeDLL%d", ddlID),  float(eflags.BC % 4), time);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing) FillHistogram("EventCounter", 2.5);
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


//______________________________________________________
Int_t QualityPhotonSelection::WhichDDL(Int_t module, Int_t cellx) const
{
	if (cellx < 1 || 64 < cellx) return -1;

	if (module < 1 || 4 < module)
	{
		printf("AliPHOSCalibration::WhichDDL module is wrong! ddl=-1 will return.\n");
		return -1;
	}

	const Int_t Nmod = 5; //totally, 5 PHOS modules are designed.
	Int_t ddl = (Nmod - module) * 4 + (cellx - 1) / 16; //convert offline module numbering to online.
	return ddl;
}
