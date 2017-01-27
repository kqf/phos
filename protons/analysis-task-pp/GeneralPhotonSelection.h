#ifndef GENERALPHOTONSELECTION_H
#define GENERALPHOTONSELECTION_H

// --- Custom header files ---
#include "PhotonSelection.h"

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>
#include <TH2F.h>
#include <TH3F.h>


// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

TString mtitle(const char * title, Int_t i)
{
	TString s = (i == 0) ? " all modules " : Form("SM%d", i);
	return Form(title, s.Data());
}

class GeneralPhotonSelection : public PhotonSelection
{
public:

	GeneralPhotonSelection(): PhotonSelection(), fListOfHistos(0) {}
	GeneralPhotonSelection(const char * name, const char * title): PhotonSelection(name, title), fListOfHistos(0) {}
	virtual ~GeneralPhotonSelection();

	virtual void InitSummaryHistograms();
	virtual void InitSelectionHistograms() = 0;
	virtual Bool_t SelectEvent(const EventFlags & flgs);
	virtual TList * GetListOfHistos() { return fListOfHistos; }


protected:
	GeneralPhotonSelection(const GeneralPhotonSelection &);
	GeneralPhotonSelection & operator = (const GeneralPhotonSelection &);

	void FillHistogram(const char * key, Double_t x, Double_t y = 1, Double_t z = 1); //Fill 3D histogram witn name key
	TList  * fListOfHistos;  //! list of histograms

private:
	ClassDef(GeneralPhotonSelection, 2)
};
#endif