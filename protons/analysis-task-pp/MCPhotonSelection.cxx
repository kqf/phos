
// #include "iterator"

// --- Custom header files ---
#include "MCPhotonSelection.h"

// --- ROOT system ---
#include <TParticle.h>
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliVCluster.h>
#include <AliAODMCParticle.h>

#include <iostream>
using namespace std;


ClassImp(MCPhotonSelection);


//________________________________________________________________
void MCPhotonSelection::FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags)
{
	(void) clusArray;
	(void) pool;
	(void) eflags;
}

//________________________________________________________________
void MCPhotonSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	(void) c1;
	(void) c2;
	(void) eflags;
}


//________________________________________________________________
void MCPhotonSelection::InitSelectionHistograms()
{
	fListOfHistos->Add(new TH1F("hZvertexGen", "Z vertex generated; z_{vtx}, cm", 200, -50., +50.));
	fListOfHistos->Add(new TH1F("hZvertexGenCut", "Z vertex generated, |z|<10; z_{vtx}, cm", 200, -50., +50.));

	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); i++)
	{
		const char * n = i->second;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_total", n), Form("Generated p_{T} total %s; p_{T}, GeV/c", n), 250, 0., 25.) );
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary", n), Form("Generated p_{T} primary %s; p_{T}, GeV/c", n), 250, 0., 25.)) ;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary", n), Form("Generated p_{T} secondary %s; p_{T}, GeV/c", n), 250, 0., 25.));
		fListOfHistos->Add(new TH2F(Form("hPtGeneratedMC_%s_total_Radius", n), Form("Generated radius, p_{T} total %s; r, cm; p_{T}, GeV/c", n), 1000, 0., 500., 250, 0., 25.));
		fListOfHistos->Add(new TH2F(Form("hPtGeneratedMC_%s_primary_Radius", n), Form("Generated radius, p_{T} primary %s; r, cm; p_{T}, GeV/c", n), 1000, 0., 500., 250, 0., 25.));
		fListOfHistos->Add(new TH2F(Form("hPtGeneratedMC_%s_secondary_Radius", n), Form("Generated radius, p_{T} secondary %s; r, cm; p_{T}, GeV/c", n), 1000, 0., 500., 250, 0., 25.));
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

}


//________________________________________________________________
void MCPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	(void) clusArray;
	(void) candidates;
	(void) eflags;
}


void MCPhotonSelection::ConsiderGeneratedParticles(TClonesArray * particles)
{

	if (! particles)
		return;

	// TODO: Add enumeration
	// TODO: Add zvertex histogram for real data
	for (Int_t i = 0; i <  particles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) particles->At(i);
		Int_t code = particle->GetPdgCode();
		const char * name = fPartNames[code];

		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		// TODO: Fill this class
		// Primary particle
		// Double_t r = particle->R() ;
		Double_t pt = particle->Pt();
		// Double_t zvtx = particle->Vz();

		// FillHistogram("hZvertexGen", zvtx);

		// TODO: how to know which particle is primary
		// if (TMath::Abs(particle->Vz()) > 10.) continue;
		// FillHistogram("hZvertexGenCut", zvtx);


		FillHistogram(Form("hPtGeneratedMC_%s_total", name), pt) ;
		// FillHistogram(Form("hPtGeneratedMC_%s_total_Radius", name), r, pt) ;

		// if (i < NPrimaryTracks)
		// {
		// 	FillHistogram(Form("hPtGeneratedMC_%s_primary", name), pt) ;
		// 	FillHistogram(Form("hPtGeneratedMC_%s_primary_Radius", name), r, pt) ;
		// }
		// else
		// {
		// 	FillHistogram(Form("hPtGeneratedMC_%s_secondary", name), pt) ;
		// 	FillHistogram(Form("hPtGeneratedMC_%s_secondary_Radius", name), r, pt) ;
		// }
	}
}