
// #include "iterator"

// --- Custom header files ---
#include "AliPP13SingleParticleQA.h"

// --- ROOT system ---
#include <TParticle.h>
#include <TProfile.h>
#include <TSystem.h>
#include <TFile.h>
#include <TTree.h>
#include <TKey.h>
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliLog.h>
#include <AliVCluster.h>
#include <AliAnalysisManager.h>

#include <iostream>
using namespace std;


ClassImp(AliPP13SingleParticleQA);


// TODO: Should I remove this method?
//________________________________________________________________
void AliPP13SingleParticleQA::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1 = ClusterMomentum(c1, eflags);
	TLorentzVector p2 = ClusterMomentum(c2, eflags);
	TLorentzVector psum = p1 + p2;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;

	Int_t sm1, sm2, x1, z1, x2, z2;
	if ((sm1 = CheckClusterGetSM(c1, x1, z1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x2, z2)) < 0) return; //  To be sure that everything is Ok


	Double_t ma12 = psum.M();
	Double_t pt12 = psum.Pt();

	fInvMass[eflags.isMixing]->Fill(ma12, pt12);
}


//________________________________________________________________
void AliPP13SingleParticleQA::InitSelectionHistograms()
{
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 20;

	// Fill Generated histograms
	for(Int_t i = 0; i < 2; ++i)
	{
		const char * ss = i == 0 ? "generated":  "reconstructed";
		
		fEtaPhi[i] = new TH2F(Form("hEtaPhi_%s", ss), Form("%s #eta vs #phi plot; #phi (rad); #eta", ss), 100, 0, TMath::Pi() * 2, 100, -1, 1);
		fListOfHistos->Add(fEtaPhi[i]);

		fPtQA[i] = new TH1F(Form("hPtQA_%s", ss), Form("%s p_{T} distribution; p_{T}, GeV/c; #frac{dN}{dp_{T}}, (GeV/c)^{-1}", ss), 1000, 0, 100);
		fListOfHistos->Add(fPtQA[i]);

		fInvMass[i] = new TH2F(Form("h%sMassPt", i == 0 ? "" : "Mix") , "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
		fListOfHistos->Add(fInvMass[i]);
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
}


void AliPP13SingleParticleQA::ConsiderGeneratedParticles(const EventFlags & flags)
{
	if (!flags.fMcParticles)
		return;

	for (Int_t i = 0; i < flags.fMcParticles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) flags.fMcParticles->At(i);
		Int_t code = TMath::Abs(particle->GetPdgCode());

		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		Double_t pt = particle->Pt();

		// pt *= Weigh(particle->E());
		fPtQA[0]->Fill(pt);
		fEtaPhi[0]->Fill(particle->Phi(), particle->Eta());

		// TODO: Don't use this flag to check QA
		// Use this to remove forward photons that can modify our true efficiency
		// if (TMath::Abs(particle->Y()) > 0.5) // NB: Use rapidity instead of pseudo rapidity!
			// continue;

		// Scale input distribution
	}
}

//________________________________________________________________
void AliPP13SingleParticleQA::FillClusterHistograms(const AliVCluster * clus, const EventFlags & eflags)
{
	TLorentzVector particle = ClusterMomentum(clus, eflags);

	fPtQA[1]->Fill(particle.Pt());
	fEtaPhi[1]->Fill(particle.Phi(), particle.Eta());
}

//________________________________________________________________
TLorentzVector AliPP13SingleParticleQA::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
    Float_t energy = c1->E();
	TLorentzVector p = AliPP13PhysPhotonSelectionMC::ClusterMomentum(c1, eflags);
    p *= Weigh(energy);
	return p;
}

//________________________________________________________________
Float_t AliPP13SingleParticleQA::Weigh(Float_t x) const
{
	return fWeighScale * (1. + fWeighA * TMath::Exp(-x / 2. * x / fWeighSigma / fWeighSigma));
}

