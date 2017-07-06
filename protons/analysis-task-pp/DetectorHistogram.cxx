// --- Custom header files ---
#include "DetectorHistogram.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TString.h>


#include <iostream>
using namespace std;


//________________________________________________________________
DetectorHistogram::DetectorHistogram(TH1 * hist, TList * owner)
{
	if (!owner->IsOwner())
		cout << "Warning: You are adding histograms to the list that doesn't have ownership" << endl;

	TString name = hist->GetName();
	const char * title = hist->GetTitle();
	for ( Int_t i = 0; i <= kLastModule; ++i)
	{
		fHistograms[i] = (i == 0) ? hist : dynamic_cast<TH1 *>( hist->Clone(name + Form("_SM%d", i)) );
		fHistograms[i]->SetTitle(Title(title, i));
		owner->Add(fHistograms[i]);
	}

	for (Int_t sm = kMinModule; sm < (kMaxModule + 1); sm++)
	{
		for (Int_t sm2 = sm; sm2 < (kMaxModule + 1); sm2++)
		{
			fModuleHistograms[sm][sm2] = dynamic_cast<TH1 *>(hist->Clone(name + Form("SM%dSM%d", sm, sm2)));
			fHistograms[i]->SetTitle(Title(title, sm, sm2));
			owner->Add(fHistograms[i]);
		}
	}
}

//________________________________________________________________
void DetectorHistogram::FillTotal(Int_t sm, Float_t x, Float_t y)
{
	if (sm < kFirstModule || sm > kLastModule)
	{
		cout << "Illegal module: " << sm << endl;
		return;
	}
	// First fill the histogram for all modules
	fHistograms[0]->Fill(x, y);
}

//________________________________________________________________
void DetectorHistogram::FillAll(Int_t sm, Float_t x, Float_t y)
{
	if (sm < kFirstModule || sm > kLastModule)
	{
		cout << "Illegal module: " << sm << endl;
		return;
	}

	FillTotal(x, y);
	// Then fill the histogram for the specific module
	fHistograms[sm]->Fill(x, y);
}

//________________________________________________________________
void DetectorHistogram::FillModules(Int_t sm1, Int_t sm2, Float_t x, Float_t y)
{
	if (sm < kFirstModule || sm > kLastModule)
	{
		cout << "Illegal module: " << sm << endl;
		return;
	}

	if (sm1 > sm2)
		swap(sm1, sm2);

	fModuleHistograms[sm1][sm2]->Fill(x, y);
}

//________________________________________________________________
TString DetectorHistogram::Title(const char * title, Int_t i) const
{
	TString s = (i == 0) ? " all modules " : Form("SM%d", i);
	return Form(title, s.Data());
}

//________________________________________________________________
TString DetectorHistogram::Title(const char * title, Int_t i, Int_t j) const
{
	TString s = (i == j) ? Form("SM%d"): Form("SM%d", i);
	return Form(title, s.Data());
}

