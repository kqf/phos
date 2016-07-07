#ifndef TESTPHOTONSELECTION_H
#define TESTPHOTONSELECTION_H
// --- Custom header files ---
#include "PhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
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
	virtual Bool_t SelectEvent(const EventFlags & flgs) {  fEvents->Fill(0.5); return kTRUE; }
	virtual TList * GetListOfHistos() { return fListOfHistos; }

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	TestPhotonSelection(const TestPhotonSelection &);
	TestPhotonSelection & operator = (const TestPhotonSelection &);

private:
	TList  * fListOfHistos;  //! list of histograms
	TH1F * fhPi0Mass[10][10];//!
	TH1F * fEvents;//!
	ClassDef(TestPhotonSelection, 2)
};
#endif