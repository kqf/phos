#ifndef CROSSMODULEHISTOGRAM_H 
#define CROSSMODULEHISTOGRAM_H 

// --- ROOT system ---
#include <TH1.h>
#include <TList.h>


// NB: Don't use common type for this class and DetectorHistogram
//     this will lead only to a confusion 

class CrossModuleHistogram
{
public:

	enum Modules {kNhists = 5, kFirstModule = 1, kLastModule=4};
	CrossModuleHistogram(): fHistograms() {}
	CrossModuleHistogram(TH1 * hist, TList * owner);

	// Default copy constructor will do the job.
	// as we don't need two copies of the same hists

	// Don't delete anything as all histograms belong to the owner
	virtual ~CrossModuleHistogram() {}

	void FillAll(Int_t sm, Int_t sm, Float_t x, Float_t y = 1.0, Float_t z = 1.0);
	TString Title(const char * title, Int_t i, Int_t j) const;


private:
	CrossModuleHistogram(const CrossModuleHistogram &);
	TH1 * fHistograms[kNhists][kNhists]; //! We are having more pointenrs than we need. 

private:
	ClassDef(CrossModuleHistogram, 2)
};
#endif