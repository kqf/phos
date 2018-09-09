// --- Custom header files ---
#include <AliPP13TriggerProperties.h>

// --- ROOT system ---

// --- AliRoot header files ---


ClassImp(AliPP13TriggerProperties);

//________________________________________________________________
AliPP13AnalysisCluster * AliPP13TriggerProperties::SelectTriggeredCluster(AliVCluster * cluster)
{
    // Coordinates of a cluster
    Float_t  position[3];
    cluster->GetPosition(position);
    TVector3 global(position);

    Int_t relid[4];
    AliPHOSGeometry::GetInstance()->GlobalPos2RelId(global, relid) ;


    AliPP13AnalysisCluster * acluster = AliPP13AnalysisCluster(cluster, kFALSE); 
    AliVCaloTrigger * fTrigger = fEvent->GetCaloTrigger("PHOS");
    fTrigger->Reset();
    while (fTrigger->Next())
    {
        if (fTrigger->GetL1TimeSum() != fL1Threshold)
            continue;

        if (Matched(fTrigger, acluster))
            return acluster;
    }

    return acluster;
}

Bool_t AliPP13TriggerProperties::Matched(AliVCaloTrigger * trigger, Int_t * relid)
{
    // "Online" module number, bottom-left 4x4 edge cell absId
    // Get the global position of the fired trigger
    Int_t trigger_module, trigger_absId;
    fTrigger->GetPosition(trigger_module, trigger_absId);

    // Convert it to local coordinates of PHOS
    Int_t trigger_relid[4] ;
    AliPHOSGeometry::GetInstance()->AbsToRelNumbering(trigger_absId, trigger_relid);

    // Returns kTRUE if cluster position coincides with 4x4 patch.
    //
    if (trigger_relid[0] != relid[0]) // different modules!
        return kFALSE;

    if (TMath::Abs(trigger_relid[2] - relid[2]) > 3) // X-distance too large!
        return kFALSE;

    if (TMath::Abs(trigger_relid[3] - relid[3]) > 3) // Z-distance too large!
        return kFALSE;

    return kTRUE;
}