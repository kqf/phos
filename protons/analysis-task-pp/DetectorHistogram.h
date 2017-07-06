#ifndef DETECTORHISTOGRAM_H 
#define DETECTORHISTOGRAM_H 

// --- ROOT system ---
#include <TH1.h>
#include <TList.h>


class DetectorHistogram
{
public:

	enum Modules {kNhists = 5, kFirstModule = 1, kLastModule=4};
	DetectorHistogram(): fHistograms() {}
	DetectorHistogram(TH1 * hist, TList * owner);

	// Default copy constructor will do the job.
	// as we don't need two copies of the same hists

	// Don't delete anything as all histograms belong to the owner
	virtual ~DetectorHistogram() {}

	void FillTotal(Float_t x, Float_t y = 1.0);
	void FillAll(Int_t sm, Float_t x, Float_t y = 1.0);
	void FillModules(Int_t sm, Int_t sm, Float_t x, Float_t y = 1.0);
	TString Title(const char * title, Int_t i) const;
	TString Title(const char * title, Int_t i, Int_t i) const;


private:
	DetectorHistogram(const DetectorHistogram &);
	TH1 * fHistograms[kNhists]; //! Keep all modules + 1 histogram for all modules
	TH1 * fModuleHistograms[kNhists][kNhists]; //! Keep all modules + 1 histogram for all modules

private:
	ClassDef(DetectorHistogram, 2)
};
#endif