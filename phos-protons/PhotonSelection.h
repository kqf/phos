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
	Double_t vtxBest[3];   // Calculated vertex position
	Int_t  centr;
	Int_t  zvtx;
};

class PhotonSelection : public TNamed
{
public:

	PhotonSelection(): TNamed() {}
	PhotonSelection(const char * name, const char * title): TNamed(name, title) {}
	virtual ~PhotonSelection() {}
	virtual void InitSummaryHistograms() = 0;
	virtual TList * GetListOfHistos() = 0; 

	virtual Bool_t SelectEvent(const EventFlags & flgs) { return kTRUE; }

	virtual void FillCellsInCluster(TObjArray * clusArray, AliVCaloCells * cells) {}
	virtual	void FillCells(AliVCaloCells * cells) {}
	virtual void FillPi0Mass(TObjArray * clusArray, const EventFlags & eflags); // implements algorithm

protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags) = 0;
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags) {}
	// TODO: Fix values (0, 9) ==> (1, 5)
	virtual Int_t CheckClusterGetSM(const AliVCluster * clus) const;

	PhotonSelection(const PhotonSelection &);
	PhotonSelection & operator = (const PhotonSelection &);

private:
	ClassDef(PhotonSelection, 1)
};
#endif