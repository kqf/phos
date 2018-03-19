#ifndef ALIPP13PION2KAONRATIO_H
#define ALIPP13PION2KAONRATIO_H


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


// NB: This will simplify the code
//

// TODO: Split this class to have separate efficiency and contamination estimators
//

class AliPP13PionToKaonRatio: public AliPP13PhysPhotonSelectionMC
{
public:
	enum Modes {kGenerated = 0, kReconstructed = 1, kNhists = 2};
	enum Particles
	{
		kPiplus = 211,
		kPiminus = -211,
		kKplus = 321,
		kKminus = -321
	};


	AliPP13PionToKaonRatio():
		AliPP13PhysPhotonSelectionMC(),
		fPrimary(),
		fAll()
	{
		fPartNames[kPiplus] = "#pi^{+}";
		fPartNames[kPiminus] = "#pi^{-}";
		fPartNames[kKplus] = "K^{+}";
		fPartNames[kKminus] = "K^{-}";
	}

	AliPP13PionToKaonRatio(const char * name, const char * title,
			AliPP13ClusterCuts cuts, AliPP13SelectionWeights * w):
		AliPP13PhysPhotonSelectionMC(name, title, cuts, w),
		fPrimary(),
		fAll()
	{
		// Force no timing cut for MC,
		// as there is no photons from different bunches
		fCuts.fTimingCut = 9999;
		fPartNames[kPiplus] = "#pi^{+}";
		fPartNames[kPiminus] = "#pi^{-}";
		fPartNames[kKplus] = "K^{+}";
		fPartNames[kKminus] = "K^{-}";
	}



	virtual void InitSelectionHistograms();
	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);

protected:
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
	{
		(void) c1;
		(void) c2;
		(void) eflags;
	}

	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;
	AliPP13PionToKaonRatio(const AliPP13PionToKaonRatio &);
	AliPP13PionToKaonRatio & operator = (const AliPP13PionToKaonRatio &);

	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames;

	typedef std::map<Int_t, TH1 *> EnumHists;
	EnumHists fPrimary;     //!
	EnumHists fAll;          //!

	// Parameters of weighed MC parametrization
	ClassDef(AliPP13PionToKaonRatio, 2)
};
#endif