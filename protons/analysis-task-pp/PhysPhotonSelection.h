#ifndef PHYSPHOTONSELECTION_H
#define PHYSPHOTONSELECTION_H
// --- Custom header files ---
#include "PhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

TString mtitle(const char * title, Int_t i)
{
	TString s = (i == 0) ? " all modules " : Form("SM%d", i);
	return Form(title, s.Data());
}

class PhysPhotonSelection : public PhotonSelection
{
public:

	PhysPhotonSelection();
	PhysPhotonSelection(const char * name, const char * title);
	virtual ~PhysPhotonSelection();

	virtual void InitSummaryHistograms();
	virtual Bool_t SelectEvent(const EventFlags & flgs);
	virtual TList * GetListOfHistos() { return fListOfHistos; }

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);

	PhysPhotonSelection(const PhysPhotonSelection &);
	PhysPhotonSelection & operator = (const PhysPhotonSelection &);

	void FillHistogram(const char * key, Double_t x, Double_t y = 1, Double_t z = 1); //Fill 3D histogram witn name key
	TList  * fListOfHistos;  //! list of histograms

private:
	ClassDef(PhysPhotonSelection, 2)
};
#endif