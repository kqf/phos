// --- Custom header files ---
#include <AliPP13SelectionWeights.h>

// --- ROOT system ---

// --- AliRoot header files ---


//________________________________________________________________
Double_t AliPP13SelectionWeights::Weight(Double_t x) const
{
	// if(!fSpectrumWeight) // Not needed
		// return 1.0;
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
	
	// Iteration 0
	// weights.fSpectrumWeight->SetParameters(2.4, 0.139, 6.880);
	// Iteration 1
    weights.fSpectrumWeight->SetParameters(0.014948507575731244, 0.2874438247098432, 9.895472915554668)

	weights.fSpectrumWeight->SetParameter(3, 0.135);
	weights.fSpectrumWeight->SetParameter(4, 0.135);
	return weights;
}

