#ifndef EFFICIENCYSELECTION_H
#define EFFICIENCYSELECTION_H


#include <map>

// --- Custom header files ---
#include "SelectionWeights.h"
#include "PhotonSelection.h"

// --- ROOT system ---
#include <TClonesArray.h>
#include <TObjArray.h>
#include <TList.h>
#include <TH1F.h>
#include <TF1.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>


class EfficiencySelection: public PhotonSelection
{
	enum Particles
	{
		kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310
	};
public:
	EfficiencySelection(): PhotonSelection(), fInvMass(), fGenerated() {}
	EfficiencySelection(const char * name, const char * title, ClusterCuts cuts, SelectionWeights * w):
		PhotonSelection(name, title, cuts, w),
		fInvMass(),
		fGenerated()
	{
		fCuts.fTimingCut = 99999; // No timing cut in MC
	}

	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);

protected:
	TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual void InitSelectionHistograms();
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;

	EfficiencySelection(const EfficiencySelection &);
	EfficiencySelection & operator = (const EfficiencySelection &);

	TH1 * fInvMass[2]; //!
	TH1 * fGenerated; //!
	ClassDef(EfficiencySelection, 2)
};
#endif