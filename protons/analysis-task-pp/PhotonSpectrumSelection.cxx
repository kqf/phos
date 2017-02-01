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

	this->SetTitle(Form("%s ## CPV = %.1f cm, Disp = %1.f cm", this->GetTitle(), fDistanceCPV, fDispersionCut));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_SM%d", i), mtitle("Cluster p_{T}, %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_cpv_SM%d", i), mtitle(TString(Form("Cluster p_{T} with CPV cut %.1f cm", fDistanceCPV)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_disp_SM%d", i), mtitle(TString(Form("Cluster p_{T} with dispersion cut %.1f cm", fDispersionCut)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for (Int_t i = 0; i < 5;  ++i)
		fListOfHistos->Add(new TH1F(Form("hClusterPt_cpv_disp_SM%d", i), mtitle(TString(Form("Cluster p_{T} with CPV %.1f cm and dispersion %.1f cm cuts", fDistanceCPV, fDispersionCut)) + ", %s; cluster p_{T}, GeV/c; counts", i), nPt, ptMin, ptMax));

	for(Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if(!hist) continue;
		hist->Sumw2();
	}	
}

//________________________________________________________________
void PhotonSpectrumSelection::FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags)
{
	Int_t x, z;
	Int_t sm = CheckClusterGetSM(clus, x, z);

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