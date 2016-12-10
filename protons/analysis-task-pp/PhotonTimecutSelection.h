#ifndef PHOTONTIMECUTSELECTION_H
#define PHOTONTIMECUTSELECTION_H

// --- Custom header files ---
#include "PhysPhotonSelection.h"

// --- ROOT header files ---
#include "TH2F.h"


class PhotonTimecutSelection : public PhysPhotonSelection
{
public:

	PhotonTimecutSelection(): PhysPhotonSelection() {}
	PhotonTimecutSelection(const char * name, const char * title): PhysPhotonSelection(name, title) {}

	virtual void InitSummaryHistograms()
	{
		if (fListOfHistos)
			AliFatal("Trying to reinitialize list of histograms");

		fListOfHistos = new TList();
		fListOfHistos->SetOwner(kTRUE);
		for (Int_t i = 0; i < 5;  ++i)
		{
			fListOfHistos->Add(new TH2F(Form("hClusterEvsTM%d", i), Form("Cluster energy vs time, M%d", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));
			fListOfHistos->Add(new TH2F(Form("hClusterPtvsTM%d", i), Form("Cluster Pt vs time, M%d", i), 100, 0., 12., 1200, -0.25 * 1e-6, 0.25 * 1e-6));
			fListOfHistos->Add(new TH2F(Form("hClusterXvsTM%d", i), Form("Cluster X vs time, M%d", i),  64, 0.5, 64.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
			fListOfHistos->Add(new TH2F(Form("hClusterZvsTM%d", i), Form("Cluster Z vs time, M%d", i),  56, 0.5, 56.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
			fListOfHistos->Add(new TH2F(Form("hClusterTimeMap%d", i), Form("Cluster time map, M%d", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
			fListOfHistos->Add(new TH2F(Form("hClusterNvsTM%d", i), Form("Cluster energy vs time, M%d", i), 25, 0.5, 25.5, 1200, -0.25 * 1e-6, 0.25 * 1e-6));
		}

	}

	virtual Bool_t SelectEvent(const EventFlags & eflags) { if (TMath::Abs(eflags.vtxBest[2]) > 10) return kFALSE; return kTRUE; }

	void SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
	{
		// Don't return TObjArray: force user to handle candidates lifetime
		Double_t pi0EClusMin = 0.3;
		Int_t sm, x, z;
		for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
		{
			AliVCluster * clus = (AliVCluster *) clusArray->At(i);
			if (clus->E() < pi0EClusMin) continue;
			if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
			candidates->Add(clus);

			// Fill histograms only for real events
			if (eflags.isMixing)
				continue;
			TLorentzVector p;
			clus->GetMomentum(p, eflags.vtxBest);

			Float_t tof = clus->GetTOF();
			FillHistogram(Form("hClusterEvsTM%d", sm), clus->E(), tof);
			FillHistogram(Form("hClusterPtvsTM%d", sm), p.Pt(), tof);
			FillHistogram(Form("hClusterXvsTM%d", sm), x, tof);
			FillHistogram(Form("hClusterZvsTM%d", sm), z, tof);
			FillHistogram(Form("hClusterTimeMap%d", sm), x, z, tof);
			FillHistogram(Form("hClusterNvsTM%d", sm), clus->GetNCells(), tof);	

			FillHistogram(Form("hClusterEvsTM%d", 0), clus->E(), tof);
			FillHistogram(Form("hClusterPtvsTM%d", 0), p.Pt(), tof);
			FillHistogram(Form("hClusterXvsTM%d", 0), x, tof);
			FillHistogram(Form("hClusterZvsTM%d", 0), z, tof);
			FillHistogram(Form("hClusterTimeMap%d", 0), x, z, tof);
			FillHistogram(Form("hClusterNvsTM%d", 0), clus->GetNCells(), tof);

		}

	}

protected:
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags) {  if (c1 && c2 && eflags.vtxBest[2]) return; }
	PhotonTimecutSelection(const PhotonTimecutSelection &);
	PhotonTimecutSelection & operator = (const PhotonTimecutSelection &);

private:
	ClassDef(PhotonTimecutSelection, 1)
};
#endif