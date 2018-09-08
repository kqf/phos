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
	AliPP13TriggerProperties(): fCluster(), fTrigger() {}
	AliPP13TriggerProperties(AliVCaloTrigger * trigger): fTrigger(fTrigger) {}

	AliPP13TriggerProperties * SelectTriggeredCluster(AliVCluster * cluster);
	Bool_t Matched(AliVCaloTrigger * trigger, AliVCluster * cluster);
	
protected:
	AliVCluster * fCluster;
	Bool_t fTrigger;

private:
	AliPP13TriggerProperties(const AliPP13TriggerProperties &);
	AliPP13TriggerProperties & operator = (const AliPP13TriggerProperties &);
};
#endif