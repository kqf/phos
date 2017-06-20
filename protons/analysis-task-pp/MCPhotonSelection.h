#ifndef MCPHOTONSELECTION_H
#define MCPHOTONSELECTION_H


#include <map>

// --- Custom header files ---
#include "GeneralPhotonSelection.h"

// --- ROOT system ---
#include <TClonesArray.h>
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>

class MCPhotonSelection: public GeneralPhotonSelection
{
public:
	enum particles{kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310, kOmega = 223, kLambda = 3122, kPPion = 211, kNPion = -211};
	MCPhotonSelection(): GeneralPhotonSelection() 
	{
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";

		// Define sources of pi0s
		fPi0SourcesNames[kK0s] = "K_{0}^s";
		fPi0SourcesNames[kLambda] = "#Lambda";
		fPi0SourcesNames[kPPion] = "#pi^{+}";
		fPi0SourcesNames[kNPion] = "#pi^{-}";	
		fPi0SourcesNames[kEta] = "#eta";
		fPi0SourcesNames[kOmega] = "#omega";

	}

	MCPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999): GeneralPhotonSelection(name, title, ec, a, n, t)
	{
		// Don't use c++11 here, as it might fail at some nodes
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";

		// Define sources of pi0s
		fPi0SourcesNames[kK0s] = "K_{0}^s";
		fPi0SourcesNames[kLambda] = "#Lambda";
		fPi0SourcesNames[kPPion] = "#pi^{+}";
		fPi0SourcesNames[kNPion] = "#pi^{-}";	
		fPi0SourcesNames[kEta] = "#eta";
		fPi0SourcesNames[kOmega] = "#omega";
	}
	virtual void InitSelectionHistograms();
    virtual void ConsiderGeneratedParticles(TClonesArray * particles, TObjArray * clusArray, const EventFlags & eflags);

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
	virtual void PythiaInfo();

	MCPhotonSelection(const MCPhotonSelection &);
	MCPhotonSelection & operator = (const MCPhotonSelection &);

	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames; 
	EnumNames fPi0SourcesNames; 

	ClassDef(MCPhotonSelection, 2)
};
#endif