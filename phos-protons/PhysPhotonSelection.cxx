// --- Custom header files ---
#include "PhysPhotonSelection.h"
// #include "AliAnalysisTaskPrompt.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

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

	// TODO: fix this for CAF
	Int_t kMinModule = 1;
	Int_t kMaxModule = 4;
	for (Int_t sm = /*AliAnalysisTaskPrompt::*/kMinModule; sm <= /*AliAnalysisTaskPrompt::*/kMaxModule; ++sm)
	{
		fListOfHistos->Add(new TH2F(Form("hMassPtSM%d", sm), Form("(M,p_{T})_{#gamma#gamma}, SM%d", sm)  , nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("hMassPtN3SM%d", sm), Form("(M,p_{T})_{#gamma#gamma}, N_{cell}>3 SM%d", sm)  , nM, mMin, mMax, nPt, ptMin, ptMax));
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

	Int_t sm1, sm2;
	if ((sm1 = CheckClusterGetSM(c1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2)) < 0) return; //  To be sure that everything is Ok

	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	if (c1->GetNCells() >= 3 && c2->GetNCells() >= 3) FillHistogram("hMassPtN3", ma12 , pt12 );
	if (c1->GetNCells() >= 4 && c2->GetNCells() >= 4) FillHistogram("hMassPtN4", ma12 , pt12 );
	if (c1->GetNCells() >= 5 && c2->GetNCells() >= 5) FillHistogram("hMassPtN5", ma12 , pt12 );
	if (c1->GetNCells() >= 6 && c2->GetNCells() >= 6) FillHistogram("hMassPtN6", ma12 , pt12 );

	if (sm1 == sm2)
		FillHistogram(Form("hMassPtSM%d", sm1), ma12, pt12);

	Bool_t three_cells_in_clusters = c1->GetNCells() >= 3 && c2->GetNCells() >= 3;
	if (!three_cells_in_clusters) return;
	if (sm1 == sm2) FillHistogram(Form("hMassPtN3SM%d", sm1), ma12, pt12);
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
		FillHistogram("hNcellsPt", clus->GetNCells(), p.Pt());
		FillHistogram("hNcellsE", clus->GetNCells(), p.E());
	}

	if (candidates->GetEntriesFast() > 1) FillHistogram("TotalDiphotonEvents", 0.5);
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
