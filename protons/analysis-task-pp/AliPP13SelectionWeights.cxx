// --- Custom header files ---
#include <AliPP13SelectionWeights.h>

// --- ROOT system ---
#include <TMath.h>

// --- AliRoot header files ---



//________________________________________________________________
Double_t AliPP13SelectionWeights::Weight(Double_t pT) const
{
	Double_t w = pT * pT * fW0 / 2. / TMath::Pi();
	Double_t fraction = (fW2 - 1.) * (fW2 - 2.) / (fW2 * fW1 * (fW2 * fW1 + fW4 * (fW2 - 2.)));
	Double_t power = TMath::Power(1. + (TMath::Sqrt(pT * pT + fW3 * fW3) - fW4) / (fW2 * fW1), -fW2);
	return w * fraction * power;
}


//________________________________________________________________
Double_t AliPP13SelectionWeights::Nonlinearity(Double_t x) const
{
	return fNonGlobal * (1. + fNonA * TMath::Exp(-x * x / 2. / fNonSigma / fNonSigma));
}
