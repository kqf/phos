#ifndef ALIPP13SELECTIONWEIGHTS_H
#define ALIPP13SELECTIONWEIGHTS_H


// --- Custom header files ---

// --- ROOT system ---
#include <TLorentzVector.h>
#include <TObject.h>
#include <TF1.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>

struct AliPP13SelectionWeights: TObject
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
private:
	ClassDef(AliPP13SelectionWeights, 2)
};

struct AliPP13SelectionWeightsMC: public AliPP13SelectionWeights
{
	Double_t Nonlinearity(Double_t x) const;

	// Parameters for Nonlinearity
	Double_t fNonGlobal;
	Double_t fNonA;
	Double_t fNonSigma;

private:
	ClassDef(AliPP13SelectionWeightsMC, 2)

};

struct AliPP13SelectionWeightsSPMC: public AliPP13SelectionWeightsMC
{
	Double_t Weight(Double_t x) const;

	// TODO: Use Shared_ptr
	static AliPP13SelectionWeights & SinglePi0();
	static AliPP13SelectionWeights & SingleEta();

	// Parameters for Nonlinearity function
	Double_t fW0;
	Double_t fW1;
	Double_t fW2;
	Double_t fW3;
	Double_t fW4;

private:
	ClassDef(AliPP13SelectionWeightsSPMC, 2)
};

#endif