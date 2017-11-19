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
	AliPP13SelectionWeights()
	{
		// fSpectrumWeight = TF1("f", "x[0] * (x[0] )*[0]/2./3.1415*([2]-1.)*([2]-2.)/([2]*[1]*([2]*[1]+[4]*([2]-2.))) * (1.+(sqrt((x[0])*(x[0])+[3]*[3])-[4])/([2]*[1])) ** (-[2])", 0, 100);
		
		// Weights 0
		// fSpectrumWeight.SetParameters(2.4, 0.139, 6.880);

		// Weights 1
	    // fSpectrumWeight.SetParameters(0.014972585670033522, 0.2858040967480923, 9.871553924028612);

		// Weights 3
	    fW0 = 0.014875782846110793;
	    fW1 = 0.28727403800708634;
	    fW2 = 9.9198075195331;

		fW3 = 0.135;
		fW4 = 0.135;

		// Nonlinearity Naive estimation
		//
		fNonGlobal = -0.022934923767457753;
		fNonA = 1.4188237289034245;
		fNonSigma = 1.0579663356860527;
	}

	Double_t Weight(Double_t x) const;
	Double_t Nonlinearity(Double_t x) const;

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