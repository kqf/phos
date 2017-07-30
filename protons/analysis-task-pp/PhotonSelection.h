#ifndef GPHOTONSELECTION_H
#define GPHOTONSELECTION_H


// --- ROOT system ---
#include <TObjArray.h>
#include "TNamed.h"
#include <TList.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliPHOSGeometry.h>
#include <AliVCluster.h>
#include <AliLog.h>

struct EventFlags
{
	enum EventType {kMB = 0, kGood = 1, kZvertex = 2, kNcontributors = 3, kTwoPhotons = 4};

	EventFlags(Int_t c = 0, Int_t z = 0, Bool_t m = kFALSE, Bool_t p = kFALSE, Bool_t vtx = kFALSE, UShort_t bc = 0. /*, Bool_t v0 = kFalse*/):
		centr(c),
		zvtx(z),
		BC(bc),
		isMixing(m),
		eventPileup(p),
		eventVtxExists(vtx),
		ncontributors(0),
		fMcParticles(0)
		//, eventV0AND(v0)
	{}

	Double_t vtxBest[3];   // Calculated vertex position
	Int_t  centr;
	Int_t  zvtx;
	UShort_t BC;
	Bool_t isMixing;
	Bool_t eventPileup;
	Bool_t eventVtxExists;
	Int_t ncontributors;
	TClonesArray * fMcParticles;

	// Bool_t eventV0AND;
};


class PhotonSelection : public TNamed
{
public:

	PhotonSelection():
		TNamed(),
		fListOfHistos(0),
		fClusterMinE(0.3),
		fAsymmetryCut(1.0),
		fNCellsCut(3)
	{}

	PhotonSelection(const char * name, const char * title, Float_t ec = 0.3, Float_t a = 1.0, Int_t n = 3, Float_t t = 999):
		TNamed(name, title),
		fListOfHistos(0),
		fClusterMinE(ec),
		fAsymmetryCut(a),
		fTimingCut(t),
		fNCellsCut(n),
		fEventCounter(0)
	{}

	virtual ~PhotonSelection();

	virtual void InitSummaryHistograms();
	virtual void InitSelectionHistograms() = 0;
	virtual Bool_t SelectEvent(const EventFlags & flgs);
	// This is a dummy method to count number of Triggered Events.
	virtual void CountMBEvent();
	virtual void FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags); // implements algorithm
    virtual void ConsiderGeneratedParticles(const EventFlags & eflags)
    {
    	(void) eflags;
    }

	virtual void MixPhotons(TObjArray & photons, TList * pool, const EventFlags & eflags);



	virtual void SetClusterMinEnergy(Float_t e) { fClusterMinE = e; }
	virtual void SetAsymmetryCut(Float_t a) { fAsymmetryCut = a; }
	virtual void SetTimingCut(Float_t t) { fTimingCut = t; }
	virtual void SetMinCellsInCluster(Float_t n) { fNCellsCut = n; }
	virtual TList * GetListOfHistos() { return fListOfHistos; }


protected:
	virtual void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags);
	virtual void FillClusterHistograms(const AliVCluster * c, const EventFlags & eflags)
	{
		(void) c;
		(void) eflags;
	}

	virtual Int_t CheckClusterGetSM(const AliVCluster * clus, Int_t & x, Int_t & z) const;
	virtual TLorentzVector ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const;

	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
	{
		(void) c1;
		(void) c2;
		(void) eflags;
	}	

	PhotonSelection(const PhotonSelection &);
	PhotonSelection & operator = (const PhotonSelection &);

	void FillHistogram(const char * key, Double_t x, Double_t y = 1, Double_t z = 1); //Fill 3D histogram witn name key
	TList  * fListOfHistos;  //! list of histograms

	Float_t fClusterMinE;
	Float_t fAsymmetryCut;
	Float_t fTimingCut;
	Int_t fNCellsCut;

	TH1 * fEventCounter;  //!
private:
	ClassDef(PhotonSelection, 2)
};
#endif