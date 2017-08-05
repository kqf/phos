#ifndef NONLINEARITYSTUDY_H
#define NONLINEARITYSTUDY_H

// --- Custom header files ---
#include "PhysPhotonSelectionMC.h"

// --- AliRoot header files ---
#include <AliVCluster.h>

class NonlinearityStudySelection : public PhysPhotonSelectionMC
{
public:
	NonlinearityStudySelection(): PhysPhotonSelectionMC() {}
	NonlinearityStudySelection(const char * name, const char * title, ClusterCuts cuts, 
		Float_t nona = 0., Float_t nonsigma = 1., Float_t genergy = 1.):
		PhysPhotonSelectionMC(name, title, cuts, nona, nonsigma, genergy)
	{
	}

    virtual void InitSelectionHistograms();
protected:
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;
	virtual Float_t Nonlinearity(Float_t x) const;

	NonlinearityStudySelection(const NonlinearityStudySelection &);
	NonlinearityStudySelection & operator = (const NonlinearityStudySelection &);

private:
	ClassDef(NonlinearityStudySelection, 2)
};
#endif