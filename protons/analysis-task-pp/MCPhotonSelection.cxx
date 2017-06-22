
// #include "iterator"

// --- Custom header files ---
#include "MCPhotonSelection.h"

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
	Float_t ptbins[] = {0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.0, 15.0, 20.0};
	Int_t ptsize = sizeof(ptbins) / sizeof(Float_t);

	// Sources of neutral pions, as a histogram
	Int_t sbins = 3222 + 3322 + 1;
	Int_t sstart = -3222;
	Int_t sstop = 3322 + 1;

	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_primary", fPartNames[kPi0].Data()), Form("Sources of primary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));
	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_secondary", fPartNames[kPi0].Data()), Form("Sources of secondary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));

	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_nocut_primary", fPartNames[kPi0].Data()), Form("Sources of primary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));
	fListOfHistos->Add(new TH1F(Form("hMC_%s_sources_nocut_secondary", fPartNames[kPi0].Data()), Form("Sources of secondary %ss ; PDG code", fPartNames[kPi0].Data()), sbins, sstart, sstop));

	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); ++i)
	{
		const char * n = (const char *) i->second.Data();

		// cout << n << endl;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_AllRange_%s", n), Form("Generated p_{T} spectrum of %ss in 4 #pi ; p_{T}, GeV/c", n), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s", n), Form("Generated p_{T} spectrum of %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary_", n), Form("Generated p_{T} spectrum of primary %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins)) ;
		fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary_", n), Form("Generated p_{T} spectrum of secondary %ss; p_{T}, GeV/c", n), ptsize - 1, ptbins));
		fListOfHistos->Add(new TH2F(Form("hPtGeneratedMC_%s_Radius", n), Form("Generated radius, p_{T} spectrum of all %ss; r, cm; p_{T}, GeV/c", n), 500, 0., 500., 400, 0, 20));

		if (i->first != kPi0)
			continue;

		for (EnumNames::iterator s = fPi0SourcesNames.begin(); s != fPi0SourcesNames.end(); s++)
		{
			const char * ns = (const char *) s->second.Data();
			fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_primary_%s", n, ns), Form("Distribution to primary #pi^{0}s from  %s decays; p_{T}, GeV/c", ns), ptsize - 1, ptbins));
			fListOfHistos->Add(new TH1F(Form("hPtGeneratedMC_%s_secondary_%s", n, ns), Form("Distribution to secondary #pi^{0}s from  %s decays; p_{T}, GeV/c", ns), ptsize - 1, ptbins));
		}

	}
	// TODO: move these files to separate selection

	TH1F * hist = new TH1F("hXsec", "xsec from pyxsec.root", 1, 0, 1);
	hist->GetXaxis()->SetBinLabel(1, "<#sigma>");
	fListOfHistos->Add(hist);

	hist = new TH1F("hTrials", "trials root file", 1, 0, 1);
	hist->GetXaxis()->SetBinLabel(1, "#sum{ntrials}");
	fListOfHistos->Add(hist);

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


void MCPhotonSelection::ConsiderGeneratedParticles(TClonesArray * particles, TObjArray * clusArray, const EventFlags & flags)
{
	if (! particles)
		return;

	// TODO: Fix this method
	// PythiaInfo();

	// TODO:
	//	 RERUN real data to get zvertex histogram
	for (Int_t i = 0; i < particles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) particles->At(i);

		// TODO: What does it mean negative PDG Code
		Int_t code = TMath::Abs(particle->GetPdgCode());
		const char * name = fPartNames[code].Data();

		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		Double_t pt = particle->Pt();

		FillHistogram(Form("hPtGeneratedMC_AllRange_%s", name), pt) ;

		// Use this to remove forward photons that can modify our true efficiency
		if (TMath::Abs(particle->Eta()) > 0.5)
			continue;

		FillHistogram(Form("hPtGeneratedMC_%s", name), pt) ;

		Double_t r = TMath::Sqrt(particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv());
		FillHistogram(Form("hPtGeneratedMC_%s_Radius", name), r, pt) ;

		Bool_t primary = IsPrimary(particle);

		if (primary)
			FillHistogram(Form("hPtGeneratedMC_%s_primary_", name), pt) ;
		else
			FillHistogram(Form("hPtGeneratedMC_%s_secondary_", name), pt) ;


		// Now estimate Pi0 sources of secondary particles
		if (code != kPi0)
			continue;

		AliAODMCParticle * parent = GetParent(i, particles);

		if (!parent)
			continue;

		Int_t pcode = parent->GetPdgCode();

		EnumNames::iterator s = fPi0SourcesNames.find(pcode);
		if (s == fPi0SourcesNames.end())
			continue;

		const char * pname = s->second.Data();

		if (!primary)
			FillHistogram(Form("hMC_%s_sources_nocut_secondary", fPartNames[kPi0].Data()), pcode);
		else
			FillHistogram(Form("hMC_%s_sources_nocut_primary", fPartNames[kPi0].Data()), pcode);


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

	// Try to extract all needed data
	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);
	for (Int_t i = 0; i < photonCandidates.GetEntries(); ++i)
		FillClusterMC(dynamic_cast<AliVCluster *>(photonCandidates.At(i)), particles);
}

//________________________________________________________________
void MCPhotonSelection::FillClusterMC(const AliVCluster * cluster, TClonesArray * particles)
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
AliAODMCParticle * MCPhotonSelection::GetParent(Int_t label, Int_t & plabel, TClonesArray * particles) const
{
	if (label <= -1)
		return 0;

	// Int_t primLabel = cluster->GetLabelAt(0) ;
	// Particle # reached PHOS front surface
	AliAODMCParticle * particle = dynamic_cast<AliAODMCParticle * >(particles->At(label));

	plabel = particle->GetMother();
	AliAODMCParticle * parent = dynamic_cast<AliAODMCParticle * >(particles->At(plabel));
	return parent;
}

//________________________________________________________________
Bool_t MCPhotonSelection::IsPrimary(const AliAODMCParticle * particle) const
{
	// Look what particle left vertex (e.g. with vertex with radius <1 cm)
	Double_t rcut = 1.;
	Double_t r2 = particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv()	;
	return r2 < rcut * rcut;
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


//________________________________________________________________
void MCPhotonSelection::PythiaInfo()
{
	// TODO: Move it to separate selection?
	// Fetch the histgram file
	TTree * tree = AliAnalysisManager::GetAnalysisManager()->GetTree();

	if (!tree)
	{
		AliError(Form("%s - UserNotify: No current tree!", GetName()));
		return;
	}

	TFile * curfile = tree->GetCurrentFile();
	if (!curfile)
	{
		AliError(Form("%s - UserNotify: No current file!", GetName()));
		return;
	}

	TString file(curfile->GetName());
	file.ReplaceAll(gSystem->BaseName(file.Data()), "");

	TFile * fxsec = TFile::Open(Form("%s%s", file.Data(), "pyxsec_hists.root"));

	if (!fxsec)
	{
		AliError(Form("There is no pyxsec_hists.root in this directory."));
		return;
	}

	// find the tlist we want to be independtent of the name so use the Tkey
	TKey * key = (TKey *)fxsec->GetListOfKeys()->At(0);
	if (!key)
		return;

	TList * list = dynamic_cast<TList *>(key->ReadObj());
	if (!list)
		return;

	Float_t xsec    = ((TProfile *)list->FindObject("h1Xsec"))  ->GetBinContent(1);
	Float_t trials  = ((TH1F *)    list->FindObject("h1Trials"))->GetBinContent(1);
	fxsec->Close();

	FillHistogram("hXsec", 0.5, xsec);
	FillHistogram("hTrials", 0.5, trials);
	// AliInfo(Form("xs %f, trial %f.\n", xsec, trials));
}