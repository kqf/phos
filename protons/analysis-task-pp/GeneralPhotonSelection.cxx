// --- Custom header files ---
#include "GeneralPhotonSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliLog.h>

#include <iostream>
using namespace std;



ClassImp(GeneralPhotonSelection);

//________________________________________________________________
void GeneralPhotonSelection::InitSummaryHistograms()
{
	// Find better place to apply this
	fListOfHistos = new TList();
	fListOfHistos->SetOwner(kTRUE);
	InitSelectionHistograms();

	TString cuts = Form(";\nCuts: |Z_{vtx}| < 10 cm, no pileup spd, E_{min}^{clu} = %.2g GeV, A =  %.2g, N_{min}^{cell} = %d, t_{clus} = %0.3g ns", fClusterMinE, fAsymmetryCut, fNCellsCut, fTimingCut * 1e+9);
	this->SetTitle(this->GetTitle() + cuts);

	cout << "Adding " << this->GetName() << ": " << this->GetTitle() << endl;


	fListOfHistos->AddFirst( new TH1C(TString("h_description_") + this->GetName(), this->GetTitle(), 1, 0, 0) ); // Very important!!! Description, dummy way
	// The true event counter
	TH1 * evntCounter = new TH1F("EventCounter", "Event cuts", 3, 0, 3);
	evntCounter->GetXaxis()->SetBinLabel(1, "all");
	evntCounter->GetXaxis()->SetBinLabel(2, "|Z_{vtx}| < 10");
	evntCounter->GetXaxis()->SetBinLabel(3, "N_{#gamma} > 2");
	fListOfHistos->AddFirst(evntCounter);

}


//________________________________________________________________
GeneralPhotonSelection::~GeneralPhotonSelection()
{
	delete fListOfHistos;
}


//________________________________________________________________
Bool_t GeneralPhotonSelection::SelectEvent(const EventFlags & flgs)
{
	// All events
	FillHistogram("EventCounter", 0.5);


	if (TMath::Abs(flgs.vtxBest[2]) > 10) return kFALSE;

	// Physical Events
	FillHistogram("EventCounter", 1.5);
	return kTRUE;
}


//________________________________________________________________
void GeneralPhotonSelection::FillHistogram(const char * key, Double_t x, Double_t y, Double_t z)
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

//________________________________________________________________
void GeneralPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		
		if (clus->GetNCells() < fNCellsCut) continue;
		if (clus->E() < fClusterMinE) continue;
		if (TMath::Abs(clus->GetTOF()) > fTimingCut) continue;
		candidates->Add(clus);

		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;

		FillClusterHistograms(clus, eflags);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		FillHistogram("EventCounter", 2.5);
}