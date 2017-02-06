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

	GeneralPhotonSelection(): PhotonSelection(), fListOfHistos(0), fClusterMinE(0.3), fAsymmetryCut(1.0), fNCellsCut(3) {}
	GeneralPhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		PhotonSelection(name, title),
		fListOfHistos(0),
		fClusterMinE(ec),
		fAsymmetryCut(a),
		fTimingCut(t),
		fNCellsCut(n)
	{}

	virtual ~GeneralPhotonSelection();

	virtual void InitSummaryHistograms();
	virtual void InitSelectionHistograms() = 0;
	virtual Bool_t SelectEvent(const EventFlags & flgs);
	virtual TList * GetListOfHistos() { return fListOfHistos; }
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void FillClusterHistograms(const AliVCluster * c, const EventFlags & eflags)
	{
		(void) c;
		(void) eflags;
	}

	void SetClusterMinEnergy(Float_t e) { fClusterMinE = e; }
	void SetAsymmetryCut(Float_t a) { fAsymmetryCut = a; }
	void SetTimingCut(Float_t t) { fTimingCut = t; }
	void SetMinCellsInCluster(Float_t n) { fNCellsCut = n; }


protected:
	GeneralPhotonSelection(const GeneralPhotonSelection &);
	GeneralPhotonSelection & operator = (const GeneralPhotonSelection &);

	void FillHistogram(const char * key, Double_t x, Double_t y = 1, Double_t z = 1); //Fill 3D histogram witn name key
	TList  * fListOfHistos;  //! list of histograms

	Float_t fClusterMinE;
	Float_t fAsymmetryCut;
	Float_t fTimingCut;
	Int_t fNCellsCut;

private:
	ClassDef(GeneralPhotonSelection, 2)
};
#endif