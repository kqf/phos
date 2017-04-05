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
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>

class MCPhotonSelection: public GeneralPhotonSelection
{
public:
	enum particles{kGamma = 22, kPi0 = 111, kEta = 221};
	MCPhotonSelection(): GeneralPhotonSelection() 
	{
		fPartNames[kGamma] = "gamma";
		fPartNames[kPi0] = "pi0";
		fPartNames[kEta] = "eta";
	}
	MCPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999): GeneralPhotonSelection(name, title, ec, a, n, t)
	{
		// Don't use c++11 here, as it might fail at some nodes
		fPartNames[kGamma] = "gamma";
		fPartNames[kPi0] = "pi0";
		fPartNames[kEta] = "eta";
	}
	virtual void InitSelectionHistograms();

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
    virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags);
    virtual void ConsiderGeneratedParticles(TClonesArray * particles);

	MCPhotonSelection(const MCPhotonSelection &);
	MCPhotonSelection & operator = (const MCPhotonSelection &);

	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames; 

	ClassDef(MCPhotonSelection, 2)
};
#endif