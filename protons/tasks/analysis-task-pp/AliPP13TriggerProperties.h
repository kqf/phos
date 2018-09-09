#ifndef ALIPP13TRIGGERPROPERTIES_H
#define ALIPP13TRIGGERPROPERTIES_H

// --- Custom header files ---
#include <AliPP13AnalysisCluster.h>

// --- ROOT system ---
#include <TObject.h>

// --- AliRoot header files ---
#include <AliVCluster.h>
#include <AliVCaloTrigger.h>

class AliPP13TriggerProperties:
{
public:
	AliPP13TriggerProperties(): fTrigger(), fL1Threshold(-1) {}
	AliPP13TriggerProperties(AliVCaloTrigger * trigger, Int_t l1threshold = -1):
		fTrigger(fTrigger),
		fL1Threshold(l1threshold)
	{}

	void FillTriggerInformation(AliPP13AnalysisCluster * cluster);
	Bool_t Matched(AliVCaloTrigger * trigger, Int_t * relid);

protected:
	AliVCaloTrigger * fTrigger;

	// L1 threshold: -1 = L0, 0 = high, 1 = medium, 2 = low
	Int_t fL1Threshold;

private:
	AliPP13TriggerProperties(const AliPP13TriggerProperties &);
	AliPP13TriggerProperties & operator = (const AliPP13TriggerProperties &);
};
#endif