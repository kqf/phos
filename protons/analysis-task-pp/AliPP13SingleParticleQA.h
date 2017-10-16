#ifndef ALIPP13MESONSELECTIONMC_H
#define ALIPP13MESONSELECTIONMC_H


#include <map>

// --- Custom header files ---
#include "AliPP13PhysPhotonSelectionMC.h"
#include "AliPP13ParticlesHistogram.h"

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



class AliPP13SingleParticleQA: public AliPP13PhysPhotonSelectionMC
{

public:
	enum Particles {kGamma = 22, kPi0 = 111, kEta = 221};
				
	AliPP13SingleParticleQA():
		AliPP13PhysPhotonSelectionMC(),
		fInvMass(),
		fEtaPhi(),
		fPtQA(),
		fWeighA(0.),
		fWeighSigma(1.),
		fWeighScale(1.)
	{
	}

	AliPP13SingleParticleQA(const char * name, const char * title, AliPP13ClusterCuts cuts, 
		Float_t nona = 0., Float_t nonsigma = 1., Float_t genergy = 1.,
		Float_t wa = 0., Float_t wsigma = 1., Float_t wscale = 1.):
		AliPP13PhysPhotonSelectionMC(name, title, cuts, nona, nonsigma, genergy),
		fInvMass(),
		fEtaPhi(),
		fPtQA(),
		fWeighA(wa),
		fWeighSigma(wsigma),
		fWeighScale(wscale)
	{
	}

	virtual void InitSelectionHistograms();
	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);
	virtual ~AliPP13SingleParticleQA()
	{
	}

protected:
	virtual void FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags);
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual Float_t Weigh(Float_t x) const;
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	AliPP13SingleParticleQA(const AliPP13SingleParticleQA &);
	AliPP13SingleParticleQA & operator = (const AliPP13SingleParticleQA &);


	TH1 * fInvMass[2];     //!
	TH1 * fEtaPhi[2];      //!
	TH1 * fPtQA[2];        //!

	// Parameters of weighed MC parametrization
	Float_t fWeighA;
	Float_t fWeighSigma;
	Float_t fWeighScale;

	ClassDef(AliPP13SingleParticleQA, 2)
};
#endif