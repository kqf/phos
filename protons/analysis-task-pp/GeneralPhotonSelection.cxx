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
	fListOfHistos->Add( new TH1C(TString("h_description_") + this->GetName(), this->GetTitle(), 1, 0, 0) ); // Very important!!! Description, dummy way

	// The true event counter
	TH1 * evntCounter = new TH1F("EventCounter", "Event cuts", 3, 0, 3);
	evntCounter->GetXaxis()->SetBinLabel(1, "all");
	evntCounter->GetXaxis()->SetBinLabel(2, "|Z_{vtx}| < 10");
	evntCounter->GetXaxis()->SetBinLabel(3, "N_{#gamma} > 2");
	fListOfHistos->Add(evntCounter);

	InitSelectionHistograms();
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