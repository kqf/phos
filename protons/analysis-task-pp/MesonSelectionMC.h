#ifndef MESONSELECTIONMC_H
#define MESONSELECTIONMC_H


#include <map>

// --- Custom header files ---
#include "GeneralPhotonSelection.h"
#include "ParticlesHistogram.h"

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


class MesonSelectionMC: public GeneralPhotonSelection
{
public:
	enum Modes {kGenerated = 0, kReconstructed = 1, kNhists = 2};
	enum Particles
	{
		kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310,
		kOmega = 223, kLambda = 3122, kPPion = 211, kNPion = -211,
		kPRho = 213, kNRho = -213,
		kKStarP = 323, kKStarN = -323, kKStar0 = 313, kBarKstar0 = -313,
		kKplus = 321, kKminus = -321, kSigmaZero = 3212
	};

	MesonSelectionMC():
		GeneralPhotonSelection(),
		fPrimaryPi0(),
		fSecondaryPi0(),
		fFeedDownPi0(),
		fInvMass()
	{
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";

		// Define sources of pi0s
		fPi0SourcesNames[kPRho] = "#rho^{+}";
		fPi0SourcesNames[kNRho] = "#rho^{-}";
		fPi0SourcesNames[kK0s] = "K^{s}_{0}";
		fPi0SourcesNames[kLambda] = "#Lambda";
		fPi0SourcesNames[kPPion] = "#pi^{+}";
		fPi0SourcesNames[kNPion] = "#pi^{-}";
		fPi0SourcesNames[kEta] = "#eta";
		fPi0SourcesNames[kOmega] = "#omega";
		fPi0SourcesNames[kKStarP] = "K^{*+}";
		fPi0SourcesNames[kKStarN] = "K^{*-}";
		fPi0SourcesNames[kKStar0] = "K^{*0}";
		fPi0SourcesNames[kBarKstar0] = "#barK^{*0}";
		fPi0SourcesNames[kKplus] = "K^{+}";
		fPi0SourcesNames[kKminus] = "K^{-}";
		fPi0SourcesNames[kSigmaZero] = "#Sigma^{0}";
	}

	MesonSelectionMC(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		GeneralPhotonSelection(name, title, ec, a, n, t),
		fPrimaryPi0(),
		fSecondaryPi0(),
		fFeedDownPi0(),
		fInvMass()

	{
		// Don't use c++11 here, as it might fail at some nodes
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";

		// Define sources of pi0s
		fPi0SourcesNames[kPRho] = "#rho^{+}";
		fPi0SourcesNames[kNRho] = "#rho^{-}";
		fPi0SourcesNames[kK0s] = "K^{s}_{0}";
		fPi0SourcesNames[kLambda] = "#Lambda";
		fPi0SourcesNames[kPPion] = "#pi^{+}";
		fPi0SourcesNames[kNPion] = "#pi^{-}";
		fPi0SourcesNames[kEta] = "#eta";
		fPi0SourcesNames[kOmega] = "#omega";
		fPi0SourcesNames[kKStarP] = "K^{*+}";
		fPi0SourcesNames[kKStarN] = "K^{*-}";
		fPi0SourcesNames[kKStar0] = "K^{*0}";
		fPi0SourcesNames[kBarKstar0] = "#barK^{*0}";
		fPi0SourcesNames[kKplus] = "K^{+}";
		fPi0SourcesNames[kKminus] = "K^{-}";
		fPi0SourcesNames[kSigmaZero] = "#Sigma^{0}";

	}

	virtual void InitSelectionHistograms();
	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);

	virtual ~MesonSelectionMC()
	{
		for (int i = 0; i < kNhists; ++i)
		{
			if (fPrimaryPi0[i]) delete fPrimaryPi0[i];
			if (fSecondaryPi0[i]) delete fSecondaryPi0[i];
			if (fFeedDownPi0[i]) delete fFeedDownPi0[i];
		}
	}

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;
	virtual AliAODMCParticle * GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const;
	virtual AliAODMCParticle * GetParent(Int_t label, TClonesArray * particles) const
	{
		Int_t plabel;
		return GetParent(label, plabel, particles);
	}
	MesonSelectionMC(const MesonSelectionMC &);
	MesonSelectionMC & operator = (const MesonSelectionMC &);

	ParticlesHistogram * fPrimaryPi0[kNhists];
	ParticlesHistogram * fSecondaryPi0[kNhists];
	ParticlesHistogram * fFeedDownPi0[kNhists];

    TH1 * fInvMass[2];                     //!
	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames;
	EnumNames fPi0SourcesNames;

	ClassDef(MesonSelectionMC, 2)
};
#endif