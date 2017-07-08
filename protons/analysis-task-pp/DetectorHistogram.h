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
	DetectorHistogram(TH1 * hist, TList * owner, Bool_t needs_modules = kFALSE);

	// Default copy constructor will do the job.
	// as we don't need two copies of the same hists

	// Don't delete anything as all histograms belong to the owner
	virtual ~DetectorHistogram() {}

	virtual void FillTotal(Float_t x, Float_t y = 1.0);
	virtual void FillAll(Int_t sm, Float_t x, Float_t y = 1.0);
	virtual void FillModules(Int_t sm1, Int_t sm2, Float_t x, Float_t y = 1.0);
	virtual TString Title(const char * title, Int_t i) const;
	virtual TString Title(const char * title, Int_t i, Int_t j) const;

protected:
	virtual Int_t Index(Int_t sm1, Int_t sm2) const;


private:
	DetectorHistogram(const DetectorHistogram &);
	TH1 * fHistograms[kNhists]; //! Keep all modules + 1 histogram for all modules
	TH1 * fModuleHistograms[kNhists]; //! Keep all modules + 1 histogram for all modules

private:
	ClassDef(DetectorHistogram, 2)
};
#endif