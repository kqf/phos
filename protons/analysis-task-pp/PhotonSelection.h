#ifndef PHOTONSELECTION_H
#define PHOTONSELECTION_H

// --- ROOT system ---
#include <TObjArray.h>
#include <TList.h>
#include <TH1D.h>
#include <TH1F.h>

// --- AliRoot header files ---
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliLog.h>

struct EventFlags
{
	EventFlags(Int_t c = 0, Int_t z = 0, Bool_t m = kFALSE, Bool_t p = kFALSE, Bool_t vtx = kFALSE/*, Bool_t v0 = kFalse*/):
		centr(c),
		zvtx(z),
		isMixing(m),
		eventPileup(p),
		eventVtxExists(vtx)
		//, eventV0AND(v0) 
		{}

	Double_t vtxBest[3];   // Calculated vertex position
	Int_t  centr;
	Int_t  zvtx;
	Bool_t isMixing;
	Bool_t eventPileup;
	Bool_t eventVtxExists;
	// Bool_t eventV0AND;
};

// Useless conditions are needed to kill unused warning.

class PhotonSelection : public TNamed
{
public:

	PhotonSelection(): TNamed() {}
	PhotonSelection(const char * name, const char * title): TNamed(name, title) {}
	virtual ~PhotonSelection() {}
	virtual void InitSummaryHistograms() = 0;
	virtual TList * GetListOfHistos() = 0;

	virtual Bool_t SelectEvent(const EventFlags & flgs) { if (flgs.zvtx > 0) return kTRUE; return kTRUE; }

	virtual void FillCellsInCluster(TObjArray * clusArray, AliVCaloCells * cells) { if (!clusArray && !cells) return;}
	virtual	void FillCells(AliVCaloCells * cells) { if (!cells) return; }
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags); // implements algorithm
	virtual void MixPhotons(TObjArray & photons, TList * pool, const EventFlags & eflags);

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags) = 0;
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags) { if (!c1 && !c2 && eflags.zvtx) return; }
	// TODO: Fix values (0, 9) ==> (1, 5)
	virtual Int_t CheckClusterGetSM(const AliVCluster * clus, Int_t & x, Int_t & z) const;

	PhotonSelection(const PhotonSelection &);
	PhotonSelection & operator = (const PhotonSelection &);

private:
	ClassDef(PhotonSelection, 1)
};
#endif