
// #include "iterator"

// --- Custom header files ---
#include "EfficiencySelection.h"


// --- ROOT system ---
#include <TParticle.h>
#include <TH1D.h>
#include <TH2D.h>

// --- AliRoot header files ---
#include <AliLog.h>
#include <AliVCluster.h>

#include <iostream>
using namespace std;


ClassImp(EfficiencySelection);


//________________________________________________________________
void EfficiencySelection::InitSelectionHistograms()
{
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	// Int_t nPt      = 400;
	// Double_t ptMin = 0;
	// Double_t ptMax = 20;

	Double_t ptBins[] = {0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.0, 15.0, 20.0};
	Int_t ptSize = sizeof(ptBins) / sizeof(Double_t);

	const char * rtitle = "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}";
	for (Int_t i = 0; i < 2; ++i)
	{
		const char * rname = Form("h%sMassPt", i == 0 ? "" : "Mix");
		fInvMass[i] = new TH2D(rname, rtitle, nM, mMin, mMax, ptSize - 1, ptBins);
		fListOfHistos->Add(fInvMass[i]);
	}
	fGenerated = new TH1D("hPt_#pi^{0}_primary_", "Generated spectrum of primary #pi^{0}", ptSize - 1, ptBins);
	fListOfHistos->Add(fGenerated);

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
}

//________________________________________________________________
void EfficiencySelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
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

	// AliAODMCParticle * origin = (AliAODMCParticle*)eflags.fMcParticles->At(0);//0 is always generated particle by AliGenBox.
	// Double_t w = fWeights->Weight(origin->Pt());
	Double_t w = fWeights->Weights(pt12, eflags);
	TH2 * hist = dynamic_cast<TH2 *> (fInvMass[eflags.isMixing]);
	hist->Fill(ma12, pt12, w);

	if (eflags.isMixing)
		return;
}

void EfficiencySelection::ConsiderGeneratedParticles(const EventFlags & eflags)
{
	if (!eflags.fMcParticles)
		return;

	for (Int_t i = 0; i < eflags.fMcParticles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) eflags.fMcParticles->At(i);
		Int_t code = TMath::Abs(particle->GetPdgCode());

		// NB: replace this condition by find, if the number of particles will grow
		//
		if (code != kPi0)
			continue;


		Double_t pt = particle->Pt();
		Double_t w = fWeights->Weights(pt, eflags);


		// Use this to remove forward photons that can modify our true efficiency
		if (TMath::Abs(particle->Y()) > 0.5) // NB: Use rapidity instead of pseudo rapidity!
			continue;


		Bool_t primary = IsPrimary(particle);

		if(!primary)
			continue;

		fGenerated->Fill(pt, w);
	}
}

//________________________________________________________________
Bool_t EfficiencySelection::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
}

//________________________________________________________________
TLorentzVector EfficiencySelection::ClusterMomentum(const AliVCluster * c1, const EventFlags & eflags) const
{
	TLorentzVector p;
	c1->GetMomentum(p, eflags.vtxBest);

	// NB: Apply nonlinearity Correction Here
	Float_t energy = c1->E();
	p *= fWeights->Nonlinearity(energy);
	return p;
}