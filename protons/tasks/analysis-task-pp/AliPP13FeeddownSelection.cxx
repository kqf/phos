
// #include "iterator"

// --- Custom header files ---
#include "AliPP13FeddownSelection.h"

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


ClassImp(AliPP13FeddownSelection);


//________________________________________________________________
void AliPP13FeddownSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
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

	if (eflags.isMixing)
		return;

	Int_t label1 = c1->GetLabelAt(0) ;
	Int_t label2 = c2->GetLabelAt(0) ;

	AliAODMCParticle * gamma_mother1 = GetParent(label1, eflags.fMcParticles);
	AliAODMCParticle * gamma_mother2 = GetParent(label2, eflags.fMcParticles);

	if (!gamma_mother1 || !gamma_mother2)
		return;

	if (gamma_mother1 != gamma_mother2)
		return;

	if (gamma_mother1->GetPdgCode() != kPi0)
		return;

	// Check if the selected \pi^{0} is primary
	//
	// Looking at the source of pi0
	Int_t source_label = gamma_mother1->GetMother();

	// It's not decay pi0
	if (source_label == -1)
		return;

	AliAODMCParticle * hadron = dynamic_cast<AliAODMCParticle *> (eflags.fMcParticles->At(source_label));

	if (!hadron)
		return;

	fFeedownK0s[0]->Fill(ma12, pt12);
}


//________________________________________________________________
void AliPP13FeddownSelection::InitSelectionHistograms()
{
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 20;

	for (Int_t i = 0; i < 2; ++i)
	{
		fInvMass[i] = new TH2F(Form("h%sMassPt", i == 0 ? "" : "Mix") , "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
		fListOfHistos->Add(fInvMass[i]);
	}
	fFeedownK0s[0] = new TH2F("MassPt_#pi^{0}_feeddown_K^{s}_{0}", "(M,p_{T})_{#gamma#gamma} originating form K^{s}_{0}; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
	fFeedownK0s[1] = new TH1F("MassPt_#pi^{0}_feeddown_K^{s}_{0}_generated", "(M,p_{T})_{#gamma#gamma} originating form K^{s}_{0}; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nPt, ptMin, ptMax);

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
}

//________________________________________________________________
AliAODMCParticle * AliPP13FeddownSelection::GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const
{
	if (label <= -1)
		return 0;

	// Int_t primLabel = cluster->GetLabelAt(0) ;
	// Particle # reached PHOS front surface
	AliAODMCParticle * particle = dynamic_cast<AliAODMCParticle * >(particles->At(label));

	if (!particle)
		return 0;

	plabel = particle->GetMother();

	if (plabel <= -1)
		return 0;

	AliAODMCParticle * parent = dynamic_cast<AliAODMCParticle * >(particles->At(plabel));
	return parent;
}

//________________________________________________________________
Bool_t AliPP13FeddownSelection::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
}

// //________________________________________________________________________
// AliAODMCParticle * AliAnalysisTaskPHOSPi0EtaToGammaGamma::GetParent(Int_t label, TClonesArray * particles) const
// {
// 	AliAODMCParticle *particle = (AliAODMCParticle*) particles->At(label);
// 	Int_t motherid = particle->GetMother();

// 	while (motherid > -1)
// 	{
// 		AliAODMCParticle *mp = (AliAODMCParticle*) particles->At(motherid);

// 		if (TMath::Abs(pdg) == target_pdg && R(mp) < 1.0) 
// 			return kTRUE;
// 		motherid = mp->GetMother();
// 	}
// 	return kFALSE;

// }