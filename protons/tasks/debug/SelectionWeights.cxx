// --- Custom header files ---
#include <SelectionWeights.h>

// --- ROOT system ---
#include <TMath.h>

// --- AliRoot header files ---


ClassImp(SelectionWeights);
ClassImp(SelectionWeightsTOF);
ClassImp(SelectionWeightsMC);
ClassImp(SelectionWeightsSPMC);

//________________________________________________________________
Double_t SelectionWeightsTOF::TofEfficiency(Double_t energy) const
{
    // TOF efficiency was parametrized as photon energy
    //
    Double_t logisitc = fLogScale / (1. + TMath::Exp(energy * fLogA + fLogB));
    Double_t expo = fExpA * TMath::Exp(energy * fExpAlpha);

    return 1. - logisitc - expo;
}


//________________________________________________________________
Double_t SelectionWeightsMC::Nonlinearity(Double_t x) const
{
    return fNonGlobal * (1. + fNonA / (1 + TMath::Power(x / fNonSigma, 2)));
}



//________________________________________________________________
Double_t SelectionWeightsSPMC::Weights(Double_t pT, const EventFlags & eflags) const
{
    // NB: Don't use origin pT
    (void) pT;
    AliAODMCParticle * origin = (AliAODMCParticle*)eflags.fMcParticles->At(0);//0 is always generated particle by AliGenBox.
    Double_t opT = origin->Pt();

    // NB: Try generating the yield instead of invariant yield
    Double_t w = /* opT * */ opT * fW0 / 2. / TMath::Pi();
    Double_t fraction = (fW2 - 1.) * (fW2 - 2.) / (fW2 * fW1 * (fW2 * fW1 + fW4 * (fW2 - 2.)));
    Double_t power = TMath::Power(1. + (TMath::Sqrt(opT * opT + fW3 * fW3) - fW4) / (fW2 * fW1), -fW2);
    return w * fraction * power;
}

//________________________________________________________________
SelectionWeights & SelectionWeightsSPMC::SinglePi0()
{
    SelectionWeightsSPMC & ws = * new SelectionWeightsSPMC();

    // The latest iteration
    //
    ws.fW0 = 0.2622666606436988 / 0.0119143016137;
    ws.fW1 = 0.08435275173194286;
    ws.fW2 = 7.356520553419461;
    ws.fW3 = 0.135;
    ws.fW4 = 0.135;

    // Start similar iteration
    // ws.fW0 = 0.6216964179825611 / 0.0989488446585;
    // ws.fW1 = 0.1327837274571318;
    // ws.fW2 = 6.656459891593017;
    // ws.fW3 = 0.135;
    // ws.fW4 = 0.135;

    ws.fNonA = -0.035;
    ws.fNonSigma = 0.95;
    ws.fNonGlobal = 1.020;
    return ws;
}


//________________________________________________________________
SelectionWeights & SelectionWeightsSPMC::SingleEta()
{
    SelectionWeightsSPMC & ws = * new SelectionWeightsSPMC();

    // NB: Note Different Parameters
    // Weights Initial (form 7 TeV paper)
    ws.fW0 = 0.201;
    ws.fW1 = 0.229;
    ws.fW2 = 7.0;
    ws.fW3 = 0.547;
    ws.fW4 = 0.547;

    // The latest nonlinarity tested on the simples data
    // ws.fNonA = -0.06;
    // ws.fNonSigma = 0.7;
    // ws.fNonGlobal = 1.015;
    
    ws.fNonA = -0.035;
    ws.fNonSigma = 0.95;
    ws.fNonGlobal = 1.020;
    return ws;
}


//________________________________________________________________
SelectionWeights & SelectionWeights::Init(Mode m)
{
    if (m == kSinglePi0MC)
        return SelectionWeightsSPMC::SinglePi0();

    if (m == kSingleEtaMC)
        return SelectionWeightsSPMC::SingleEta();

    if (m == kMC)
        return * new SelectionWeightsMC();

    if (m == kData)
        return * new SelectionWeightsTOF();

    return * new SelectionWeights();
}
