#ifndef ALIPP13MESONSELECTIONMC_H
#define ALIPP13MESONSELECTIONMC_H


#include <map>

// --- Custom header files ---
#include "AliPP13PhysPhotonSelectionMC.h"
#include "AliPP13ParticlesHistogram.h"
#include "AliPP13SelectionWeights.h"

// --- ROOT system ---
#include <TClonesArray.h>
#include <TObjArray.h>
#include <TList.h>
#include <TF1.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>



class AliPP13FeddownSelection: public AliPP13PhysPhotonSelectionMC
{
public:
	enum Particles
	{
		kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310,
		kOmega = 223, kLambda = 3122, kPPion = 211, kNPion = -211,
		kPRho = 213, kNRho = -213,
		kKStarP = 323, kKStarN = -323, kKStar0 = 313, kBarKstar0 = -313,
		kKplus = 321, kKminus = -321, kSigmaZero = 3212
	};

	AliPP13FeddownSelection():
		AliPP13PhysPhotonSelectionMC(),
		fInvMass(),
		fFeedownK0s()
	{
	}

	AliPP13FeddownSelection(const char * name, const char * title, 
			AliPP13ClusterCuts cuts, AliPP13SelectionWeights * w):
		AliPP13PhysPhotonSelectionMC(name, title, cuts, w),
		fInvMass(),
		fFeedownK0s()
	{
	}

	virtual void InitSelectionHistograms();
	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);

protected:
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;
	virtual AliAODMCParticle * GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const;
	virtual AliAODMCParticle * GetParent(Int_t label, TClonesArray * particles) const
	{
		Int_t plabel;
		return GetParent(label, plabel, particles);
	}
	void ConsiderGeneratedPi0(Int_t i, Double_t pt, Bool_t primary, const EventFlags & flags);

	AliPP13FeddownSelection(const AliPP13FeddownSelection &);
	AliPP13FeddownSelection & operator = (const AliPP13FeddownSelection &);

	TH1 * fInvMass[2];     //!
	TH1 * fFeedownK0s[2];  //!

	// Parameters of weighed MC parametrization
	ClassDef(AliPP13FeddownSelection, 2)
};
#endif