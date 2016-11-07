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
	if (TMath::Abs(flgs.vtxBest[2]) > 10) return kFALSE;
	FillHistogram("TotalEvents", 0.5);
	return kTRUE;
}

//________________________________________________________________
void PhysPhotonSelection::InitSummaryHistograms()
{
	fListOfHistos = new TList();
	// fListOfHistos->SetName("Data");
	fListOfHistos->SetOwner(kTRUE);
	fListOfHistos->Add( new TH1C(TString("h_description_") + this->GetName(), this->GetTitle(), 1, 0, 0) ); // Very important!!! Description, dummy way
	fListOfHistos->Add( new TH1F("TotalEvents", "Total number of analysed events", 1, 0, 1) );
	fListOfHistos->Add( new TH1F("TotalDiphotonEvents", "Total number of events with 2 photons", 1, 0, 1) );

	// pi0 mass spectrum
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 40;

	fListOfHistos->Add(new TH2F("hMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hNcellsPt", "Cell multiplicity; N_{cell}; p_{T}, GeV/c" , 41, 0, 40, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hNcellsE", "Cell multiplicity; N_{cell}; E, GeV" , 41, 0, 40, nPt, ptMin, ptMax));


	fListOfHistos->Add(new TH2F("hMixMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4"  , nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5"  , nM, mMin, mMax, nPt, ptMin, ptMax));

	// TODO: fix this for CAF
	Int_t kMinModule = 1;
	Int_t kMaxModule = 4;

	for (Int_t sm = kMinModule; sm < (kMaxModule + 1); sm++)
		for (Int_t sm2 = sm; sm2 < (kMaxModule + 1); sm2++)
			fListOfHistos->Add(new TH2F(Form("hMassPtSM%dSM%d", sm, sm2), "(M,p_{T})_{#gamma#gamma}; m_{#gamma #gamma}, GeV/c^{2} ; p_{T}, GeV/c"  , nM, mMin, mMax, nPt, ptMin, ptMax));

	for (Int_t sm = kMinModule; sm < (kMaxModule + 1); sm++)
		for (Int_t sm2 = sm; sm2 < (kMaxModule + 1); sm2++)
			fListOfHistos->Add(new TH2F(Form("hMixMassPtSM%dSM%d", sm, sm2), "(M,p_{T})_{#gamma#gamma}; m_{#gamma #gamma}, GeV/c^{2} ; p_{T}, GeV/c"  , nM, mMin, mMax, nPt, ptMin, ptMax));
}

//________________________________________________________________
void PhysPhotonSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

	// Only physical clusters
    if(c1->GetNCells() < 3 || c2->GetNCells() < 3) return;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;
	// if (psum.Pt() < 2.) return;

	Int_t sm1, sm2;
	if ((sm1 = CheckClusterGetSM(c1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	if(pt12 < 1) return;

	const char * suff = eflags.isMixing ? "Mix" : "";
	if (c1->GetNCells() >= 3 && c2->GetNCells() >= 3) FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 4 && c2->GetNCells() >= 4) FillHistogram(Form("h%sMassPtN4", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 5 && c2->GetNCells() >= 5) FillHistogram(Form("h%sMassPtN5", suff), ma12 , pt12 );
	if (c1->GetNCells() >= 6 && c2->GetNCells() >= 6) FillHistogram(Form("h%sMassPtN6", suff), ma12 , pt12 );

	if(sm1 < sm2)
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm1, sm2), ma12, pt12);
	else
		FillHistogram(Form("h%sMassPtSM%dSM%d", suff, sm2, sm1), ma12, pt12);

}

//________________________________________________________________
void PhysPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Double_t pi0EClusMin = 0.3;
	Int_t sm;
	TLorentzVector p;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->E() < pi0EClusMin) continue;
		if ((sm = CheckClusterGetSM(clus)) < 0) continue;
		candidates->Add(clus);

		clus->GetMomentum(p, eflags.vtxBest);

		if (!eflags.isMixing)
		{
			FillHistogram("hNcellsPt", clus->GetNCells(), p.Pt());
			FillHistogram("hNcellsE", clus->GetNCells(), p.E());
		}
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing) FillHistogram("TotalDiphotonEvents", 0.5);
}

//________________________________________________________________
void PhysPhotonSelection::FillHistogram(const char * key, Double_t x, Double_t y, Double_t z)
{
	//FillHistogram
	TObject * obj = fListOfHistos->FindObject(key);

	TH1 * th1 = dynamic_cast<TH1 *> (obj);
	if (th1)
	{
		th1->Fill(x, y);
		return;
	}

	TH2 * th2 = dynamic_cast<TH2 *> (obj);
	if (th2)
	{
		th2->Fill(x, y, z);
		return;
	}
	TH3 * th3 = dynamic_cast<TH3 *> (obj);
	if (th3)
	{
		th3->Fill(x, y, z);
		return;
	}

	AliError(Form("Can't find histogram (instance of TH*) <%s> ", key));
}
