// --- Custom header files ---
#include <AliPP13SelectionWeights.h>

// --- ROOT system ---

// --- AliRoot header files ---


//________________________________________________________________
Double_t AliPP13SelectionWeights::Weight(Double_t x) const
{
	(void) x;
	if(!fSpectrumWeight) // Not needed
		return 1.0;

	return fSpectrumWeight->Eval(x);
}


//________________________________________________________________
Double_t AliPP13SelectionWeights::Nonlinearity(Double_t x) const
{
	(void) x;
	if(!fNonlinearity) // Not needed
		return 1.0;

	// Not implemented
	return 1.0;
}

//________________________________________________________________
AliPP13SelectionWeights AliPP13SelectionWeights::GetWeigtsSPMC()
{
	AliPP13SelectionWeights weights;

	weights.fSpectrumWeight = new TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100);
	weights.fSpectrumWeight->SetParameters(2.4, 0.139, 6.880);
	weights.fSpectrumWeight->SetParameter(3, 0.135);
	weights.fSpectrumWeight->SetParameter(4, 0.135);
	return weights;
}

