#ifndef ALIPP13SELECTIONWEIGHTS_H
#define ALIPP13SELECTIONWEIGHTS_H


// --- Custom header files ---

// --- ROOT system ---
#include <TLorentzVector.h>
#include <TObjArray.h>
#include <TList.h>
#include <TF1.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>

struct AliPP13SelectionWeights
{
	enum Mode {kData, kMC, kSinglePi0MC, kSingleEtaMC};

	Double_t Weight(Double_t x) const 
	{ 
		(void) x;
		return 1.0; 
	}

	Double_t Nonlinearity(Double_t x) const 
	{
		(void) x;
		return 1.0; 
	}

	// TODO: Use Shared_ptr
	static AliPP13SelectionWeights & Init(Mode m);
};

struct AliPP13SelectionWeightsSPMC: public AliPP13SelectionWeights
{
	Double_t Weight(Double_t x) const;
	Double_t Nonlinearity(Double_t x) const;

	// TODO: Use Shared_ptr
	static AliPP13SelectionWeights & SinglePi0();

	// Parameters for Nonlinearity function
	Double_t fW0;
	Double_t fW1;
	Double_t fW2;
	Double_t fW3;
	Double_t fW4;

	// Parameters for Nonlinearity
	Double_t fNonGlobal;
	Double_t fNonA;
	Double_t fNonSigma;

};

#endif