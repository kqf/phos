/ --- Custom header files ---
#include "CrossModuleHistogram.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TString.h>


#include <iostream>
using namespace std;


//________________________________________________________________
CrossModuleHistogram::CrossModuleHistogram(TH1 * hist, TList * owner)
{
	if (!owner->IsOwner())
		cout << "Warning: You are adding histograms to the list that doesn't have ownership" << endl;

	TString name = hist->GetName();
	const char * title = hist->GetTitle();
	for( Int_t i = kFirstModule; i <= kLastModule; ++i)
	{
		for( Int_t j = kFirstModule; i <= kLastModule; ++i)
		{
			if(j < i)
				continue;
			fHistograms[i][j] = (i == 0) ? hist: dynamic_cast<TH1 *>( hist->Clone(name + Form("_SM%dSM%d", i, j)) );
			fHistograms[i][j]->SetTitle(Title(title, i, j));
			owner->Add(fHistograms[i][j]);
		}
	}

}

//________________________________________________________________
void CrossModuleHistogram::FillAll(Int_t sm1, Int_t sm2, Float_t x, Float_t y, Float_t z)
{
	if(sm1 < kFirstModule || sm1 > kLastModule)
	{
		cout << "Illegal module: " << sm1 << endl;
		return;
	}

	if(sm2 < kFirstModule || sm2 > kLastModule)
	{
		cout << "Illegal module: " << sm1 << endl;
		return;
	}	

	// Just ignore the same modules
	Int_t i = sm1 < sm2 ? sm1 : sm2;
	Int_t j = sm1 > sm2 ? sm1 : sm2;

	// TODO: Add possibility for the 3d histograms
	fHistograms[i][j]->Fill(x, y);
}

//________________________________________________________________
TString CrossModuleHistogram::Title(const char * title, Int_t i, Int_t j) const
{
	TString s = (i == j) ? Fomr("SM%d", i) : Form("SM%dSM%d", i, j);
	return Form(title, s.Data());
}

