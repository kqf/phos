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
	for( Int_t i = 0; i <= kLastModule; ++i)
	{
		fHistograms[i] = (i == 0) ? hist: dynamic_cast<TH1 *>( hist->Clone(name + Form("_SM%d", i)) );
		fHistograms[i]->SetTitle(Title(title, i));
		owner->Add(fHistograms[i]);
	}

}

//________________________________________________________________
void DetectorHistogram::FillAll(Int_t sm, Float_t x, Float_t y, Float_t z)
{
	if(sm < kFirstModule || sm > kLastModule)
	{
		cout << "Illegal module: " << sm << endl;
		return;
	}
	// First fill the histogram for all modules
	fHistograms[0]->Fill(x, y);

	// Then fill the histogram for the specific module
	fHistograms[sm]->Fill(x, y);
}

//________________________________________________________________
TString DetectorHistogram::Title(const char * title, Int_t i) const
{
	TString s = (i == 0) ? " all modules " : Form("SM%d", i);
	return Form(title, s.Data());
}

