// --- Custom header files ---
#include "PhotonSpectrumSelection.h"
// #include "AliAnalysisTaskPP.h"

// --- ROOT system ---
#include <TH2F.h>
#include <TH3F.h>

// --- AliRoot header files ---
#include <AliPHOSGeometry.h>

#include <iostream>
using namespace std;

Bool_t TestLambda(Double_t l1, Double_t l2, Double_t R)
{
	// TODO: Check these parameters
	Double_t l1Mean = 1.22 ;
	Double_t l2Mean = 2.0 ;
	Double_t l1Sigma = 0.42 ;
	Double_t l2Sigma = 0.71 ;
	Double_t c = -0.59 ;
	Double_t R2 = (l1 - l1Mean) * (l1 - l1Mean) / l1Sigma / l1Sigma + (l2 - l2Mean) * (l2 - l2Mean) / l2Sigma / l2Sigma - c * (l1 - l1Mean) * (l2 - l2Mean) / l1Sigma / l2Sigma;
	return (R2 < R * R) ;
}


ClassImp(PhotonSpectrumSelection);

//________________________________________________________________
void PhotonSpectrumSelection::InitSelectionHistograms()
{

	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 40;

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_SM%d", i), mtitle("Cluster p_{T}, %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_cpv_SM%d", i), mtitle(TString(Form("Cluster p_{T} with CPV cut %.1f cm", fDistanceCPV)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_disp_SM%d", i), mtitle(TString(Form("Cluster p_{T} with dispersion cut %.1f cm", fDispersionCut)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_cpv_disp_SM%d", i), mtitle(TString(Form("Cluster p_{T} with CPV %.1f cm and dispersion %.1f cm cuts", fDistanceCPV, fDispersionCut)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));
}

//________________________________________________________________
void PhotonSpectrumSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{

	// TODO: Do we need to invoke this function for mixing?
	// Don't return TObjArray: force user to handle candidates lifetime

	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);

		if (clus->GetNCells() < fNCellsCut) continue;
		if (clus->E() < fClusterMinE) continue;
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		if (TMath::Abs(clus->GetTOF()) > fTimingCut) continue;
		candidates->Add(clus);


		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;

		TLorentzVector p;
		clus->GetMomentum(p, eflags.vtxBest);

		FillHistogram(Form("hClusterPt_SM%d", 0), p.Pt());
		FillHistogram(Form("hClusterPt_SM%d", sm), p.Pt());

		Bool_t cpv = clus->GetEmcCpvDistance() > fDistanceCPV;
		if (cpv)
		{
			FillHistogram(Form("hClusterPt_cpv_SM%d", 0), p.Pt());
			FillHistogram(Form("hClusterPt_cpv_SM%d", sm), p.Pt());
		}

		Bool_t disp = TestLambda(clus->GetM20(), clus->GetM02(), fDispersionCut);
		
		if (disp)
		{
			FillHistogram(Form("hClusterPt_disp_SM%d", 0), p.Pt());
			FillHistogram(Form("hClusterPt_disp_SM%d", sm), p.Pt());
		}

		if (cpv && disp)
		{
			FillHistogram(Form("hClusterPt_cpv_disp_SM%d", 0), p.Pt());
			FillHistogram(Form("hClusterPt_cpv_disp_SM%d", sm), p.Pt());
		}

	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		FillHistogram("EventCounter", 2.5);
}

