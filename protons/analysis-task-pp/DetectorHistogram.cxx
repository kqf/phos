// --- Custom header files ---
#include "DetectorHistogram.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TString.h>


#include <iostream>
using namespace std;


//
//________________________________________________________________
DetectorHistogram::DetectorHistogram(TH1 * hist, TList * owner, Mode mode):
	fMode(mode)

{
	if (!owner->IsOwner())
		cout << "Warning: You are adding histograms to the list that doesn't have ownership" << endl;

	TString name = hist->GetName();
	const char * title = hist->GetTitle();
	for ( Int_t i = 0; i < 2; ++i)
	{
		fHistograms[i] = (i == 0) ? hist : dynamic_cast<TH1 *>( hist->Clone(name + "SM123") );
		fHistograms[i]->SetTitle(Title(title, i));
		owner->Add(fHistograms[i]);
	}

	if (mode == kOnlyHist)
		return;

	if (mode == kModules)
	{
		for (Int_t sm = kFirstModule; sm < (kLastModule + 1); ++sm)
		{
			fModuleHistograms[sm] = dynamic_cast<TH1 *>(hist->Clone(name + Form("SM%d", sm)));
			fModuleHistograms[sm]->SetTitle(Title(title, sm, sm));
			owner->Add(fModuleHistograms[sm]);
		}
		return;
	}

	for (Int_t sm = kFirstModule; sm < (kLastModule + 1); ++sm)
	{
		for (Int_t sm2 = sm; sm2 < (kLastModule + 1); ++sm2)
		{
			fInterModuleHistograms[Index(sm, sm2)] = dynamic_cast<TH1 *>(hist->Clone(name + Form("SM%dSM%d", sm, sm2)));
			fInterModuleHistograms[Index(sm, sm2)]->SetTitle(Title(title, sm, sm2));
			owner->Add(fInterModuleHistograms[Index(sm, sm2)]);
		}
	}
}


//________________________________________________________________
void DetectorHistogram::FillAll(Int_t sm1, Int_t sm2, Float_t x, Float_t y)
{
	if (sm1 < kFirstModule || sm1 > kLastModule)
	{
		cout << "Illegal module: " << sm1 << endl;
		return;
	}

	if (sm2 < kFirstModule || sm2 > kLastModule)
	{
		cout << "Illegal module: " << sm2 << endl;
		return;
	}

	fHistograms[0]->Fill(x, y);

	// Fill histograms without specific Module
	if (sm1 != 4 &&  sm2 != 4)
		fHistograms[1]->Fill(x, y);

	FillModules(sm1, sm2, x, y);
}

//________________________________________________________________
void DetectorHistogram::FillModules(Int_t sm1, Int_t sm2, Float_t x, Float_t y)
{

	if(sm1 == sm2 && fMode == kModules)
		fModuleHistograms[sm1]->Fill(x, y);

	if (fMode == kInterModules)
		fInterModuleHistograms[Index(sm1, sm2)]->Fill(x, y);
}

//________________________________________________________________
TString DetectorHistogram::Title(const char * title, Int_t i) const
{
	TString s = (i == 0) ? " all modules " : "modules 1, 2, 3";
	return Form(title, s.Data());
}

//________________________________________________________________
TString DetectorHistogram::Title(const char * title, Int_t i, Int_t j) const
{
	TString s = (i == j) ? Form("Module %d", i) : Form("SM%dSM%d", i, j);
	return Form(title, s.Data());
}

//________________________________________________________________
Int_t DetectorHistogram::Index(Int_t sm1, Int_t sm2) const
{
	if (sm1 > sm2)
		swap(sm1, sm2);

	// TODO: Get rid of this loop here
	Int_t index = 0;
	for (Int_t i = kFirstModule; i < (kLastModule + 1); ++i)
	{
		for (Int_t j = i; j < (kLastModule + 1); ++j)
		{
			if (i == sm1 && j == sm2)
				return index;
			++index;
		}
	}
	return -1;
}