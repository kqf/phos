// --- Custom header files ---
#include <AliPP13TriggerProperties.h>

// --- ROOT system ---

// --- AliRoot header files ---


ClassImp(AliPP13TriggerProperties);

//________________________________________________________________
AliPP13TriggerProperties::operator AliVCluster * ()
{
    return fCluster;
}

void AliPP13TriggerProperties::SelectTriggeredCluster(AliVCluster * cluster)
{
    AliVCaloTrigger * trg = fEvent->GetCaloTrigger("PHOS");
    trg->Reset();
    while (trg->Next())
    {
        if (trg->GetL1TimeSum() != L1)
            continue;

        if (Matched(trigger, cluster))
            return AliPP13AnalysisCluster(cluster, kTRUE);
    }

    return AliPP13AnalysisCluster(cluster, kFALSE);
}

Bool_t AliPP13TriggerProperties::Matched(AliVCaloTrigger * trigger, AliVCluster * cluster)
{
    fPHOSGeo->GlobalPos2RelId(global1, relId);
    return kTRUE;
}