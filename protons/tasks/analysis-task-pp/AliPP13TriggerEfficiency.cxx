// --- Custom header files ---
#include "AliPP13TriggerEfficiency.h"
#include "AliPP13DetectorHistogram.h"

// --- ROOT system ---
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(AliPP13TriggerEfficiency);

//________________________________________________________________
void AliPP13TriggerEfficiency::SelectTwoParticleCombinations(const TObjArray & photonCandidates, const EventFlags & eflags)
{
	// NB: Trigger efficiency is a function of a photon registration efficiency
	//     therefore the histograms should be filled for each photon.

	// Consider N^2 - N combinations, excluding only same-same clusters.
	for (Int_t i = 0; i < photonCandidates.GetEntriesFast(); i++)
	{
		AliVCluster * tag = dynamic_cast<AliVCluster *> (photonCandidates.At(i));

		// TODO: Implement the trigger cluster selection
		if (false)
			continue;

		for (Int_t j = 0; j < photonCandidates.GetEntriesFast(); j++)
		{
			if (i == j) // Skip the same clusters
				continue;

			AliVCluster * probe = dynamic_cast<AliVCluster *> (photonCandidates.At(j));

			if (!fCuts.AcceptPair(tag, probe, eflags))
				continue;

			ConsiderPair(tag, probe, eflags);
		} // second cluster loop
	} // cluster loop}
}


//________________________________________________________________
void AliPP13TriggerEfficiency::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;
	Float_t energy = p2.E();
	Float_t m12 = psum.M();


	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok


	// TODO: Implement the GetTruFunction
	// 

	Int_t tru = 0;
	Int_t mix = int(eflags.isMixing);

	fTotalMassEnergyAll[mix]->Fill(m12, energy);
	fMassEnergyAll[tru][mix]->FillAll(sm1, sm2, m12, energy);

	if (false)
		return;

	fTotalMassEnergyTrigger[mix]->Fill(m12, energy);
	fMassEnergyTrigger[tru][mix]->FillAll(sm1, sm2, m12, energy);
}


//________________________________________________________________
void AliPP13TriggerEfficiency::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 250;
	Double_t mMin  = 0.0;
	Double_t mMax  = 0.3;

	Int_t nE      = 2000;
	Double_t eMin = 0;
	Double_t eMax = 20;

	for (Int_t i = 0; i < 2; ++i)
	{
		const char * sf = (i == 0) ? "" : "Mix";
		const char * title = "(M_{#gamma#gamma}, E_{probe}); M_{#gamma#gamma}, GeV; E_{probe}, GeV";

		fTotalMassEnergyAll[i] = new TH2F(Form("h%sMassEnergyAll", sf), title, nM, mMin, mMax, nE, eMin, eMax);
		fTotalMassEnergyTrigger[i] = new TH2F(Form("h%sMassEnergyTrg", sf), title, nM, mMin, mMax, nE, eMin, eMax);

		fListOfHistos->Add(fTotalMassEnergyAll[i]);
		fListOfHistos->Add(fTotalMassEnergyTrigger[i]);
	}


	for (Int_t tru = 0; tru < kTRUs; ++tru)
	{
		for (Int_t i = 0; i < 2; ++i)
		{
			const char * sf = (i == 0) ? "" : "Mix";
			const char * title = Form("(M_{#gamma#gamma}, E_{probe}) TRU #%d ; M_{#gamma#gamma}, GeV; E_{probe}, GeV", tru);
			TH2F * hist1 = new TH2F(Form("h%sMassEnergyAll_TRU_%d_", sf, tru), title, nM, mMin, mMax, nE, eMin, eMax);
			TH2F * hist2 = new TH2F(Form("h%sMassEnergyTrg_TRU_%d_", sf, tru), title, nM, mMin, mMax, nE, eMin, eMax);

			fMassEnergyAll[tru][i] = new AliPP13DetectorHistogram(hist1, fListOfHistos, AliPP13DetectorHistogram::kSingleHist);
			fMassEnergyTrigger[tru][i] = new AliPP13DetectorHistogram(hist2, fListOfHistos, AliPP13DetectorHistogram::kSingleHist);
		}
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

}