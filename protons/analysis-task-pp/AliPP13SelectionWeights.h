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
		fSpectrumWeight = new TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100);
		
		// Weights 0
		// fSpectrumWeight->SetParameters(2.4, 0.139, 6.880);

		// Weights 1
	    weights.fSpectrumWeight->SetParameters(0.014972585670033522, 0.2858040967480923, 9.871553924028612);
		fSpectrumWeight->SetParameter(3, 0.135);
		fSpectrumWeight->SetParameter(4, 0.135);
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