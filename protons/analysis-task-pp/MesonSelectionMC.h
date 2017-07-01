#ifndef MESONSELECTIONMC_H 
#define MESONSELECTIONMC_H 


#include <map>

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

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
	enum particles{kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310, kOmega = 223, kLambda = 3122, kPPion = 211, kNPion = -211, kPRho = 213, kNRho = -213};
	MesonSelectionMC(): GeneralPhotonSelection()
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

	}

	MesonSelectionMC(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999): GeneralPhotonSelection(name, title, ec, a, n, t)
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
	}
	
	virtual void InitSelectionHistograms();
    virtual void ConsiderGeneratedParticles(TObjArray * clusArray, const EventFlags & eflags);

    virtual ~MesonSelectionMC()
    {
    	if(fMassPt) delete	fMassPt;
    	if(fWidthPt) delete	fWidthPt;
    }

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
    virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags);

	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;
	virtual AliAODMCParticle * GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const;
	virtual AliAODMCParticle * GetParent(Int_t label, TClonesArray * particles) const
	{
		Int_t plabel;
		return GetParent(label, plabel, particles);
	}
	virtual void FillClusterMC(const AliVCluster * cluster, TClonesArray * particles);

	MesonSelectionMC(const MesonSelectionMC &);
	MesonSelectionMC & operator = (const MesonSelectionMC &);

	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames; 
	EnumNames fPi0SourcesNames; 

	// Pt-parametrizations for mass and width
	TF1 * fMassPt;     //!
	TF1 * fWidthPt;    //!

	ClassDef(MesonSelectionMC, 2)
};
#endif