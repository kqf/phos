#ifndef ALIPP13TRIGGEREFFICIENCY_H
#define ALIPP13TRIGGEREFFICIENCY_H

// --- Custom header files ---
#include "AliPP13PhysicsSelection.h"
#include "AliPP13DetectorHistogram.h"
#include "AliPP13SelectionWeights.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class AliPP13TriggerEfficiency: public AliPP13PhysicsSelection
{
	enum {kTRUs=7};
public:
	AliPP13TriggerEfficiency():
		AliPP13PhysicsSelection(),
		fMassEnergyAll(),
		fMassEnergyTrigger()
	{
	}

	AliPP13TriggerEfficiency(const char * name, const char * title, AliPP13ClusterCuts cuts, AliPP13SelectionWeights * w):
		AliPP13PhysicsSelection(name, title, cuts, w),
		fMassEnergyAll(),
		fMassEnergyTrigger()
	{
	}

	virtual void InitSelectionHistograms();
	
protected:
	virtual void SelectTwoParticleCombinations(const TObjArray & photonCandidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	AliPP13TriggerEfficiency(const AliPP13TriggerEfficiency &);
	AliPP13TriggerEfficiency & operator = (const AliPP13TriggerEfficiency &);
private:
	TH1 * fTotalMassEnergyAll[2]; //!
	TH1 * fTotalMassEnergyTrigger[2]; //!

	AliPP13DetectorHistogram * fMassEnergyAll[kTRUs][2]; //!
	AliPP13DetectorHistogram * fMassEnergyTrigger[kTRUs][2]; //!
	ClassDef(AliPP13TriggerEfficiency, 2)
};
#endif