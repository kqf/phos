// --- Custom header files ---
#include <AliPP13AnalysisCluster.h>

// --- ROOT system ---

// --- AliRoot header files ---


ClassImp(AliPP13AnalysisCluster);

//________________________________________________________________
AliPP13AnalysisCluster::operator AliVCluster * ()
{
    return fCluster;
}

