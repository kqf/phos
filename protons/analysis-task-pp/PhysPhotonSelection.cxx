// --- Custom header files ---
#include "PhysPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

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


ClassImp(PhysPhotonSelection);

PhysPhotonSelection::PhysPhotonSelection():
	PhotonSelection(), fListOfHistos(0) {}

//________________________________________________________________
PhysPhotonSelection::PhysPhotonSelection(const char * name, const char * title):
	PhotonSelection(name, title),
	fListOfHistos(0) {}

//________________________________________________________________
PhysPhotonSelection::~PhysPhotonSelection()
{
	delete fListOfHistos;
}

//________________________________________________________________
Bool_t PhysPhotonSelection::SelectEvent(const EventFlags & flgs)
{
	// All events
	FillHistogram("EventCounter", 0.5);

	if (TMath::Abs(flgs.vtxBest[2]) > 10) return kFALSE;

	// Physical Events
	FillHistogram("EventCounter", 1.5);
	return kTRUE;
}

//________________________________________________________________
void PhysPhotonSelection::InitSummaryHistograms()
{
	// Find better place to apply this
	fListOfHistos = new TList();
	fListOfHistos->SetOwner(kTRUE);
	fListOfHistos->Add( new TH1C(TString("h_description_") + this->GetName(), this->GetTitle(), 1, 0, 0) ); // Very important!!! Description, dummy way

	// The true event counter
	TH1 * evntCounter = new TH1F("EventCounter", "Event cuts", 3, 0, 3);
	evntCounter->GetXaxis()->SetBinLabel(1, "all");
	evntCounter->GetXaxis()->SetBinLabel(2, "|Z_{vtx}| < 10");
	evntCounter->GetXaxis()->SetBinLabel(3, "N_{#gamma} > 2");

	fListOfHistos->Add(evntCounter);

	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 500;
	Double_t ptMin = 0;
	Double_t ptMax = 100;

	fListOfHistos->Add(new TH2F("hMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));



	fListOfHistos->Add(new TH2F("hMixMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));

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

	// Info about selected clusters
	fListOfHistos->Add(new TH2F("hNcellsPt", "Cell multiplicity; N_{cell}; p_{T}, GeV/c" , 41, 0, 40, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hNcellsE", "Cell multiplicity; N_{cell}; E, GeV" , 41, 0, 40, nPt, ptMin, ptMax));

	// Heatmap check for physics + check abs Id numbering
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_0_SM%d", i), mtitle("Cluster N(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_0_SM%d", i), mtitle("Cluster E(Id), %s, E < 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdN_1_SM%d", i), mtitle("Cluster N(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));
	for (Int_t i = 1; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterIdE_1_SM%d", i), mtitle("Cluster E(Id), %s, E > 1 GeV", i), 3584, 0.5 + (i - 1) * 3584 , i * 3584  + 0.5));

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

	if (pt12 < 1) return;

	const char * suff = eflags.isMixing ? "Mix" : "";
	if (c1->GetNCells() >= 3 && c2->GetNCells() >= 3) FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 4 && c2->GetNCells() >= 4) FillHistogram(Form("h%sMassPtN4", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 5 && c2->GetNCells() >= 5) FillHistogram(Form("h%sMassPtN5", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 6 && c2->GetNCells() >= 6) FillHistogram(Form("h%sMassPtN6", suff), ma12 , pt12 );

	if (sm1 < sm2)
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm1, sm2), ma12, pt12);
	else
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm2, sm1), ma12, pt12);
}

//________________________________________________________________
void PhysPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
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

		// Float_t timesigma = 12.5e-9; // 12.5 ns
		// if (TMath::Abs(clus->GetTOF()) > timesigma)
		// 	continue;

		FillHistogram(Form("hMainClusterEnergy_SM%d", 0), p.E());
		FillHistogram(Form("hMainClusterEnergy_SM%d", sm), p.E());


		FillHistogram(Form("hCluNXZM_%d_SM%d", isHighECluster, sm), x, z, 1.);
		FillHistogram(Form("hCluEXZM_%d_SM%d", isHighECluster, sm), x, z, energy);

		for (Int_t c = 0; c < clus->GetNCells(); ++c)
		{
			FillHistogram(Form("hClusterIdN_%d_SM%d", isHighECluster, sm), clus->GetCellAbsId(c));
			FillHistogram(Form("hClusterIdE_%d_SM%d", isHighECluster, sm), clus->GetCellAbsId(c), energy);
		}
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing) FillHistogram("EventCounter", 2.5);
}

//________________________________________________________________
void PhysPhotonSelection::FillHistogram(const char * key, Double_t x, Double_t y, Double_t z)
{
	//FillHistogram
	TObject * obj = fListOfHistos->FindObject(key);

	TH3 * th3 = dynamic_cast<TH3 *> (obj);
	if (th3)
	{
		th3->Fill(x, y, z);
		return;
	}

	TH2 * th2 = dynamic_cast<TH2 *> (obj);
	if (th2)
	{
		th2->Fill(x, y, z);
		return;
	}

	TH1 * th1 = dynamic_cast<TH1 *> (obj);
	if (th1)
	{
		th1->Fill(x, y);
		return;
	}

	AliError(Form("Can't find histogram (instance of TH*) <%s> ", key));
}