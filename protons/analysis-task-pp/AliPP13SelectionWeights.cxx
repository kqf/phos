// --- Custom header files ---
#include <AliPP13SelectionWeights.h>

// --- ROOT system ---

// --- AliRoot header files ---

// NB: Keep these methods for different parametrizations
//

//________________________________________________________________
Double_t AliPP13SelectionWeights::Weight(Double_t x) const
{
	// if(!fSpectrumWeight) // Not needed
		// return 1.0;
	return fSpectrumWeight.Eval(x);
}


//________________________________________________________________
Double_t AliPP13SelectionWeights::Nonlinearity(Double_t x) const
{
	// (void) x;
	// if(!fNonlinearity) // Not needed
		// return 1.0;

	// Not implemented
	// return 1.0;
	return fNonlinearity.Eval(x);
}
