
// #include "iterator"

// --- Custom header files ---
#include "MCPhotonSelection.h"

// --- ROOT system ---
#include <TParticle.h>
#include <TH2F.h>

// --- AliRoot header files ---
#include <AliLog.h>
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
	// fListOfHistos->Add(new TH1F("hZvertexGen", "Z vertex generated; z_{vtx}, cm", 200, -50., +50.));
	// fListOfHistos->Add(new TH1F("hZvertexGenCut", "Z vertex generated, |z|<10; z_{vtx}, cm", 200, -50., +50.));

	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); i++)
	{
		const char * n = (const char *) i->second.Data();
		cout << n << endl;
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

	fListOfHistos->Add(new TH1F("hLatePrimaryParticles", "Particles with E > 5 GeV and tof > 0.15 ns; PDG code", 6000, 0.5, 6000.5));
}


void MCPhotonSelection::ConsiderGeneratedParticles(TClonesArray * particles, TObjArray * clusArray, const EventFlags & flags)
{

	if (! particles)
		return;

	// TODO: Add enumeration
	// TODO: Add zvertex histogram for real data
	for (Int_t i = 0; i <  particles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) particles->At(i);
		Int_t code = particle->GetPdgCode();
		const char * name = fPartNames[code].Data();

		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		// TODO: Fill this class
		// Primary particle
		// Double_t r = particle->R() ;
		Double_t pt = particle->Pt();
		//Primary particle
		Double_t r = TMath::Sqrt(particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv());
		// if (r > rcut)

		// Double_t zvtx = particle->Vz();

		// FillHistogram("hZvertexGen", zvtx);

		// TODO: how to know which particle is primary
		// if (TMath::Abs(particle->Vz()) > 10.) continue;
		// FillHistogram("hZvertexGenCut", zvtx);


		FillHistogram(Form("hPtGeneratedMC_%s_total", name), pt) ;
		FillHistogram(Form("hPtGeneratedMC_%s_total_Radius", name), r, pt) ;

		if (r < 1)
		{
			FillHistogram(Form("hPtGeneratedMC_%s_primary", name), pt) ;
			FillHistogram(Form("hPtGeneratedMC_%s_primary_Radius", name), r, pt) ;
		}
		else
		{
			FillHistogram(Form("hPtGeneratedMC_%s_secondary", name), pt) ;
			FillHistogram(Form("hPtGeneratedMC_%s_secondary_Radius", name), r, pt) ;
		}
	}

	// Try to extract all needed data

	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);
	for(Int_t i = 0; i < photonCandidates.GetEntries(); ++i)
		FillClusterMC(dynamic_cast<AliVCluster *>(photonCandidates.At(i)), particles);

}

//________________________________________________________________
void MCPhotonSelection::FillClusterMC(const AliVCluster * cluster, TClonesArray * particles)
{
	// Particle # reached PHOS front surface	
	Int_t primLabel = cluster->GetLabelAt(0) ; 
	Double_t rcut = 1;
	AliAODMCParticle * parent = 0;


	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	if (primLabel > -1)
	{
		AliAODMCParticle * prim = (AliAODMCParticle*)particles->At(primLabel) ;
		Int_t iparent = primLabel;
		parent = prim;
		Double_t r2 = prim->Xv() * prim->Xv() + prim->Yv() * prim->Yv() ;
		while ((r2 > rcut * rcut) && (iparent > -1))
		{
			iparent = parent->GetMother();
			parent = (AliAODMCParticle*)particles->At(iparent);
			r2 = parent->Xv() * parent->Xv() + parent->Yv() * parent->Yv() ;
		}
	}

	if(cluster->GetTOF() > 0.15e-6 && cluster->E() > 5)
		FillHistogram("hLatePrimaryParticles", parent->GetPdgCode());

}

//________________________________________________________________
void MCPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime
	Int_t sm, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if ((sm = CheckClusterGetSM(clus, x, z)) < 0) continue;
		
		if (clus->GetNCells() < fNCellsCut) continue;
		if (clus->E() < fClusterMinE) continue;

		// IMPORTANT: Don't apply timing cuts for MC 
		// if (TMath::Abs(clus->GetTOF()) > fTimingCut) continue;
		candidates->Add(clus);

		// Fill histograms only for real events
		if (eflags.isMixing)
			continue;
		// There is no cluster histograms here
		// FillClusterHistograms(clus, eflags);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		FillHistogram("EventCounter", 4.5);
}