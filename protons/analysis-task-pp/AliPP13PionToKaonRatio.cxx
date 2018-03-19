
// #include "iterator"

// --- Custom header files ---
#include "AliPP13PionToKaonRatio.h"

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


ClassImp(AliPP13PionToKaonRatio);


//________________________________________________________________
void AliPP13PionToKaonRatio::InitSelectionHistograms()
{
	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); ++i)
	{
		fAll[i->first] = new TH1F(Form("hPt_%s_", i->second.Data()), Form("Generated Spectrum of %s; p_{T}, GeV/c", i->second.Data()), 200, 0, 20);
		fPrimary[i->first] = new TH1F(Form("hPt_%s_primary", i->second.Data()), Form("Generated Spectrum of primary %s; p_{T}, GeV/c", i->second.Data()), 200, 0, 20);
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
}


void AliPP13PionToKaonRatio::ConsiderGeneratedParticles(const EventFlags & flags)
{
	if (!flags.fMcParticles)
		return;

	for (Int_t i = 0; i < flags.fMcParticles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) flags.fMcParticles->At(i);
		Int_t code = TMath::Abs(particle->GetPdgCode());

		// NB: replace this condition by find, if the number of particles will grow
		//
		if (fAll.find(code) == fAll.end())
			continue;

		Double_t pt = particle->Pt();
		fAll[code]->Fill(pt);

		if (IsPrimary(particle))
			fPrimary[code]->Fill(pt);
	}
}


//________________________________________________________________
Bool_t AliPP13PionToKaonRatio::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
}

