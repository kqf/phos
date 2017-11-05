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
	AliPP13SelectionWeights():
		fSpectrumWeight(0),
		fNonlinearity(0)
	{
	}

	~AliPP13SelectionWeights()
	{
		if(fNonlinearity)
			delete fNonlinearity;

		if(fSpectrumWeight)
			delete fSpectrumWeight;
	}

	AliPP13SelectionWeights(const AliPP13SelectionWeights & other):
		fSpectrumWeight(0),
		fNonlinearity(0)
	{
		this->Copy(other);
	}

	AliPP13SelectionWeights & operator=(const AliPP13SelectionWeights & other)
	{
		this->Copy(other);
		return *this;
	}


	static AliPP13SelectionWeights GetWeigtsSPMC();

	Double_t Weight(Double_t x) const;
	Double_t Nonlinearity(Double_t x) const;


	TF1	* fSpectrumWeight; //!
	TF1	* fNonlinearity; //!

private:
	void Copy(const AliPP13SelectionWeights & other)
	{
		if(other.fSpectrumWeight)
			this->fSpectrumWeight = dynamic_cast<TF1 *> (other.fSpectrumWeight->Clone());

		if(other.fNonlinearity)
			this->fNonlinearity = dynamic_cast<TF1 *> (other.fNonlinearity->Clone());
	}
};

#endif