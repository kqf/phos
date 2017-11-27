// --- Custom header files ---
#include <AliPP13SelectionWeights.h>

// --- ROOT system ---
#include <TMath.h>

// --- AliRoot header files ---



//________________________________________________________________
Double_t AliPP13SelectionWeightsSPMC::Weight(Double_t pT) const
{
	Double_t w = pT * pT * fW0 / 2. / TMath::Pi();
	Double_t fraction = (fW2 - 1.) * (fW2 - 2.) / (fW2 * fW1 * (fW2 * fW1 + fW4 * (fW2 - 2.)));
	Double_t power = TMath::Power(1. + (TMath::Sqrt(pT * pT + fW3 * fW3) - fW4) / (fW2 * fW1), -fW2);
	return w * fraction * power;
}


//________________________________________________________________
Double_t AliPP13SelectionWeightsSPMC::Nonlinearity(Double_t x) const
{
	return fNonGlobal * (1. + fNonA * TMath::Exp(-x * x / 2. / fNonSigma / fNonSigma));
}



//________________________________________________________________
AliPP13SelectionWeights & AliPP13SelectionWeightsSPMC::SinglePi0()
{
    AliPP13SelectionWeightsSPMC & ws = * new AliPP13SelectionWeightsSPMC();

    // Weights 3
    ws.fW0 = 0.014875782846110793;
    ws.fW1 = 0.28727403800708634;
    ws.fW2 = 9.9198075195331;

    ws.fW3 = 0.135;
    ws.fW4 = 0.135;

    // Nonlinearity Naive estimation
    //
    // ws.fNonGlobal = -0.022934923767457753;
    // ws.fNonA = 1.4188237289034245;
    // ws.fNonSigma = 1.0579663356860527;

    ws.fNonGlobal = 1.0;
    ws.fNonA = 0;
    ws.fNonSigma = 1.0579663356860527;

    return ws;
}

//________________________________________________________________
AliPP13SelectionWeights & AliPP13SelectionWeights::Init(Mode m)
{
    if(m == kSinglePi0MC)
        return AliPP13SelectionWeightsSPMC::SinglePi0();
    
    return * new AliPP13SelectionWeights();
}
