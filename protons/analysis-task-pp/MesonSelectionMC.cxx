
// #include "iterator"

// --- Custom header files ---
#include "MesonSelectionMC.h"

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


ClassImp(MesonSelectionMC);


//________________________________________________________________
void MesonSelectionMC::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
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

	const char * suff = eflags.isMixing ? "Mix" : "";
	FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12);


	Int_t label1 = c1->GetLabelAt(0) ;
	Int_t label2 = c2->GetLabelAt(0) ;

	AliAODMCParticle * mother1 = GetParent(label1, eflags.fMcParticles);
	AliAODMCParticle * mother2 = GetParent(label2, eflags.fMcParticles);

	if (!mother1 || !mother2)
		return;

	if (mother1 != mother2)
		return;

	if (mother1->GetPdgCode() != kPi0)
		return;

	// Check if the selected \pi^{0} is primary
	//
	Bool_t primary = IsPrimary(mother1);

	// Looking at the source of pi0
	//
	AliAODMCParticle * hadron = dynamic_cast<AliAODMCParticle *> (eflags.fMcParticles->At(mother1->GetMother()));
	Int_t hcode = hadron->GetPdgCode();

	if (!hadron)
		return;

	if (primary)
		FillHistogram("hMassPtN3_primary_", ma12, pt12);
	else
		FillHistogram("hMassPtN3_secondary_", ma12, pt12);


	EnumNames::iterator s = fPi0SourcesNames.find(hcode);
	if (s == fPi0SourcesNames.end())
		return;

	const char * pname = s->second.Data();

	if (primary)
		FillHistogram(Form("hMassPtN3_primary_%s", pname), ma12, pt12);
	else
		FillHistogram(Form("hMassPtN3_secondary_%s", pname), ma12, pt12);
}


//________________________________________________________________
void MesonSelectionMC::InitSelectionHistograms()
{
	Int_t nM       = 750;
	Double_t mMin  = 0.0;
	Double_t mMax  = 1.5;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 20;

	fListOfHistos->Add(new TH2F("hMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMixMassPtN3", "Mixed (M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));


	Float_t ptbins[] = {0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.0, 15.0, 20.0};
	Int_t ptsize = sizeof(ptbins) / sizeof(Float_t);

	// Sources of neutral pions, as a histogram
	Int_t sbins = 3222 + 3322 + 1;
	Int_t sstart = -3222;
	Int_t sstop = 3322 + 1;

	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_primary", fPartNames[kPi0].Data()), Form("Sources of primary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));
	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_secondary", fPartNames[kPi0].Data()), Form("Sources of secondary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));

	// Fill reconstruction histograms
	//
	fListOfHistos->Add(new TH2F("hMassPtN3_primary_", "(M,p_{T})_{#gamma#gamma} primary , N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));
	fListOfHistos->Add(new TH2F("hMassPtN3_secondary_", "(M,p_{T})_{#gamma#gamma} secondary , N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax));

	for (EnumNames::iterator s = fPi0SourcesNames.begin(); s != fPi0SourcesNames.end(); s++)
	{
		const char * ns = (const char *) s->second.Data();
		fListOfHistos->Add(new TH2F(Form("hMassPtN3_primary_%s", ns), Form("(M,p_{T})_{#gamma#gamma} primary %s, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", ns), nM, mMin, mMax, nPt, ptMin, ptMax));
		fListOfHistos->Add(new TH2F(Form("hMassPtN3_secondary_%s", ns), Form("(M,p_{T})_{#gamma#gamma} secondary %s, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", ns), nM, mMin, mMax, nPt, ptMin, ptMax));
	}

	// Fill Generated histograms
	const char * np = fPartNames[kPi0];
	fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary_", np), "Distribution of primary #pi^{0}s; p_{T}, GeV/c", ptsize - 1, ptbins));
	fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary_", np), "Distribution of secondary #pi^{0}s; p_{T}, GeV/c", ptsize - 1, ptbins));

	for (EnumNames::iterator s = fPi0SourcesNames.begin(); s != fPi0SourcesNames.end(); s++)
	{
		const char * ns = (const char *) s->second.Data();
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary_%s", np, ns), Form("Distribution to primary #pi^{0}s from  %s decays; p_{T}, GeV/c", ns), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary_%s", np, ns), Form("Distribution to secondary #pi^{0}s from  %s decays; p_{T}, GeV/c", ns), ptsize - 1, ptbins));
	}

	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); ++i)
	{
		const char * n = (const char *) i->second.Data();

		// cout << n << endl;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_AllRange_%s", n), Form("Generated p_{T} spectrum of %ss in 4 #pi ; p_{T}, GeV/c", n), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH2F(Form("hPtGeneratedMC_%s_Radius", n), Form("Generated radius, p_{T} spectrum of all %ss; r, cm; p_{T}, GeV/c", n), 500, 0., 500., 400, 0, 20));
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s", n), Form("Generated p_{T} spectrum of %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary_", n), Form("Generated p_{T} spectrum of primary %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins)) ;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary_", n), Form("Generated p_{T} spectrum of secondary %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins));

	}
	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

	fListOfHistos->Add(new TH1F("hPrimaryParticles", "Primary Particles; PDG code", 6000, 0.5, 6000.5));
	fListOfHistos->Add(new TH1F("hEnergeticParticles", "Primary Particles with E > 1 GeV, and tof > 0.05 ns; PDG code", 6000, 0.5, 6000.5));
	fListOfHistos->Add(new TH1F("hLatePrimaryParticles", "Primalry Particles with E > 5 GeV and tof > 0.15 ns; PDG code", 6000, 0.5, 6000.5));
}


void MesonSelectionMC::ConsiderGeneratedParticles(TClonesArray * clusArray, const EventFlags & flags)
{
	if (!flags.fMcParticles)
		return;

	// TODO:
	//	 RERUN real data to get zvertex histogram
	for (Int_t i = 0; i < flags.fMcParticles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) flags.fMcParticles->At(i);

		Int_t code = TMath::Abs(particle->GetPdgCode());
		const char * name = fPartNames[code].Data();

		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		Double_t pt = particle->Pt();

		FillHistogram(Form("hPtGeneratedMC_AllRange_%s", name), pt) ;

		// Use this to remove forward photons that can modify our true efficiency
		// Use Rapidity instead of pseudo rapidity
		//
		if (TMath::Abs(particle->Y()) > 0.5)
			continue;

		FillHistogram(Form("hPtGeneratedMC_%s", name), pt) ;

		Double_t r = TMath::Sqrt(particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv());
		FillHistogram(Form("hPtGeneratedMC_%s_Radius", name), r, pt) ;

		Bool_t primary = IsPrimary(particle);

		if (primary)
			FillHistogram(Form("hPtGeneratedMC_%s_primary_", name), pt) ;
		else
			FillHistogram(Form("hPtGeneratedMC_%s_secondary_", name), pt) ;


		// Now estimate Pi0 sources of secondaryflags.fMcParticles
		if (code != kPi0)
			continue;

		AliAODMCParticle * parent = GetParent(i, flags.fMcParticles);

		if (!parent)
			continue;

		Int_t pcode = parent->GetPdgCode();

		EnumNames::iterator s = fPi0SourcesNames.find(pcode);
		if (s == fPi0SourcesNames.end())
			continue;

		const char * pname = s->second.Data();

		// Reject MIPS and count again
		if (pt < 0.3)
			continue;

		if (!primary)
		{
			FillHistogram(Form("hMC_%s_sources_secondary", fPartNames[kPi0].Data()), pcode);
			FillHistogram(Form("hPtGeneratedMC_%s_secondary_%s", name, pname), pt) ;
			continue;
		}

		FillHistogram(Form("hMC_%s_sources_primary", fPartNames[kPi0].Data()), pcode);
		FillHistogram(Form("hPtGeneratedMC_%s_primary_%s", name, pname), pt) ;
	}
}

//________________________________________________________________
void MesonSelectionMC::FillClusterMC(const AliVCluster * cluster, TClonesArray * particles)
{
	// Particle # reached PHOS front surface
	Int_t label = cluster->GetLabelAt(0) ;

	if (label <= -1)
		return;

	AliAODMCParticle * parent = dynamic_cast<AliAODMCParticle *> (particles->At(label));

	while ((!IsPrimary(parent)) && (label > -1))
		parent = GetParent(label, label, particles);

	if (!parent)
		return;

	FillHistogram("hPrimaryParticles", parent->GetPdgCode());

	if (cluster->GetTOF() > 0.05e-6 && cluster->E() > 1)
		FillHistogram("hEnergeticParticles", parent->GetPdgCode());

	if (cluster->GetTOF() > 0.15e-6 && cluster->E() > 5)
		FillHistogram("hLatePrimaryParticles", parent->GetPdgCode());

}

//________________________________________________________________
AliAODMCParticle * MesonSelectionMC::GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const
{
	if (label <= -1)
		return 0;

	// Int_t primLabel = cluster->GetLabelAt(0) ;
	// Particle # reached PHOS front surface
	AliAODMCParticle * particle = dynamic_cast<AliAODMCParticle * >(particles->At(label));

	if (!particle)
		return 0;

	plabel = particle->GetMother();
	AliAODMCParticle * parent = dynamic_cast<AliAODMCParticle * >(particles->At(plabel));
	return parent;
}

//________________________________________________________________
Bool_t MesonSelectionMC::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
}


//________________________________________________________________
void MesonSelectionMC::SelectPhotonCandidates(const TClonesArray * clusArray, TClonesArray * candidates, const EventFlags & eflags)
{
	// Don't return TClonesArray: force user to handle candidates lifetime
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

		// TODO: Redefine Cluster Histogram?
		// There is no cluster histograms here
		// FillClusterHistograms(clus, eflags);
		FillClusterMC(clus, eflags.fMcParticles);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		FillHistogram("EventCounter", 4.5);
}