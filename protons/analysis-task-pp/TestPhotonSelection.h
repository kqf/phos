#ifndef TESTPHOTONSELECTION_H
#define TESTPHOTONSELECTION_H
// --- Custom header files ---
#include "PhotonSelection.h"
#include "DetectorHistogram.h"

// --- ROOT system ---
#include <TList.h>
#include <TH1F.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

class TestPhotonSelection : public PhotonSelection
{
public:

	TestPhotonSelection();
	TestPhotonSelection(const char * name, const char * title);
	virtual ~TestPhotonSelection();

	virtual void InitSummaryHistograms();
	virtual Bool_t SelectEvent(const EventFlags & flgs) {  fEvents->Fill(0.5); return PhotonSelection::SelectEvent(flgs); }
	virtual TList * GetListOfHistos() { return fListOfHistos; }
	
	// This selection doesn't require mixing
	virtual void MixPhotons(TClonesArray & p, TList * pl, const EventFlags & e) { if(p.GetEntries() && pl && e.isMixing) return; }

protected:
	virtual void SelectPhotonCandidates(const TClonesArray * clusArray, TClonesArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	TestPhotonSelection(const TestPhotonSelection &);
	TestPhotonSelection & operator = (const TestPhotonSelection &);

private:
	TH1F * fEvents;//!
	TList  * fListOfHistos;  //! list of histograms
	DetectorHistogram fhPi0Mass;
	ClassDef(TestPhotonSelection, 2)
};
#endif