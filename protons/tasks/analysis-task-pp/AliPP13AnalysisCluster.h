#ifndef ALIPP13ANALYSISCLUSTER_H
#define ALIPP13ANALYSISCLUSTER_H

// --- Custom header files ---

// --- ROOT system ---
#include <TObject.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

class AliPP13AnalysisCluster: public TObject
{
public:
	AliPP13AnalysisCluster(): fCluster(), fTrigger() {}
	AliPP13AnalysisCluster(AliVCluster * c, Bool_t t): fCluster(c), fTrigger(t) {}
	operator AliVCluster * ();
	
protected:
	AliVCluster * fCluster;
	Bool_t fTrigger;

private:
	AliPP13AnalysisCluster(const AliPP13AnalysisCluster &);
	AliPP13AnalysisCluster & operator = (const AliPP13AnalysisCluster &);

	ClassDef(AliPP13AnalysisCluster, 1)
};
#endif