
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


// TODO: Refactor the monster methods for pi0


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

	fInvMass[eflags.isMixing]->Fill(ma12, pt12);

	if (eflags.isMixing)
		return;

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

	if (primary)
		fPrimaryPi0[kReconstructed]->FillS(ma12, pt12);
	else
		fSecondaryPi0[kReconstructed]->FillS(ma12, pt12);

	// Looking at the source of pi0
	Int_t source_label = mother1->GetMother();

	// It's not decay pi0
	if (source_label == -1)
		return;

	AliAODMCParticle * hadron = dynamic_cast<AliAODMCParticle *> (eflags.fMcParticles->At(source_label));

	if (!hadron)
		return;

	Int_t hcode = hadron->GetPdgCode();

	if (primary)
	{
		fPrimaryPi0[kReconstructed]->Fill(hcode, ma12, pt12);
		return;
	}

	if (!IsPrimary(hadron))
	{
		fSecondaryPi0[kReconstructed]->Fill(hcode, ma12, pt12);
		return;
	}

	fFeedDownPi0[kReconstructed]->FillAll(hcode, ma12, pt12);
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

	for (Int_t i = 0; i < 2; ++i)
	{
		fInvMass[i] = new TH2F(Form("h%sMassPt", i == 0 ? "" : "Mix") , "(M,p_{T})_{#gamma#gamma}, N_{cell}>2; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
		fListOfHistos->Add(fInvMass[i]);
	}


	Float_t ptbins[] = {0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.0, 15.0, 20.0};
	Int_t ptsize = sizeof(ptbins) / sizeof(Float_t);

	// Sources of neutral pions, as a histogram
	for (int i = 0; i < 2; ++i)
	{
		Int_t sstart = -10000;
		Int_t sstop = 10000 + 1;
		Int_t sbins = sstop - sstart;

		const char * s = (i == 0) ? "secondary" : "primary";
		fPi0Sources[i] = new TH1F(Form("hMC_%s_sources_%s", fPartNames[kPi0].Data(), s), Form("Sources of %s %ss ; PDG code", s, fPartNames[kPi0].Data()), sbins, sstart, sstop);
		fListOfHistos->Add(fPi0Sources[i]);
	}

	// Fill Generated histograms
	const char * np = fPartNames[kPi0];
	TH1 * hist = new TH1F(Form("hPt_%s_primary_", np), "Distribution of primary #pi^{0}s from primary ; p_{T}, GeV/c", ptsize - 1, ptbins);
	fPrimaryPi0[kGenerated] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);

	hist = new TH1F(Form("hPt_%s_secondary_", np), "Distribution of secondary #pi^{0}s from secondary ; p_{T}, GeV/c", ptsize - 1, ptbins);
	fSecondaryPi0[kGenerated] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);

	hist = new TH1F(Form("hPt_%s_feeddown_", np), "Distribution of primary #pi^{0}s from secondary ; p_{T}, GeV/c", ptsize - 1, ptbins);
	fFeedDownPi0[kGenerated] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);

	hist = new TH2F(Form("hMassPt_%s_primary_", np), "(M,p_{T})_{#gamma#gamma} from primary ; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
	fPrimaryPi0[kReconstructed] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);

	hist = new TH2F(Form("hMassPt_%s_secondary_", np), "(M,p_{T})_{#gamma#gamma} from secondary ; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
	fSecondaryPi0[kReconstructed] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);

	hist = new TH2F(Form("hMassPt_%s_feeddown_", np), "(M,p_{T})_{#gamma#gamma} from secondary ; M_{#gamma#gamma}, GeV; p_{T}, GeV/c", nM, mMin, mMax, nPt, ptMin, ptMax);
	fFeedDownPi0[kReconstructed] = new ParticlesHistogram(hist, fListOfHistos, fPi0SourcesNames);


	for (EnumNames::iterator i = fPartNames.begin(); i != fPartNames.end(); ++i)
	{
		const char * n = (const char *) i->second.Data();
		fSpectrums[i->first] = new ParticleSpectrum(n, fListOfHistos, ptsize - 1, ptbins, i->first != kPi0);
	}

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}
}


void MesonSelectionMC::ConsiderGeneratedParticles(const EventFlags & flags)
{
	if (!flags.fMcParticles)
		return;

	// TODO: RERUN real data to get zvertex histogram
	for (Int_t i = 0; i < flags.fMcParticles->GetEntriesFast(); i++)
	{
		AliAODMCParticle * particle = ( AliAODMCParticle *) flags.fMcParticles->At(i);
		Int_t code = TMath::Abs(particle->GetPdgCode());

		// NB: replace this condition by find, if the number of particles will grow
		//
		if (code != kGamma && code != kPi0 && code != kEta)
			continue;

		Double_t pt = particle->Pt();
		fSpectrums[code]->fPtAllRange->Fill(pt);

		// Use this to remove forward photons that can modify our true efficiency
		if (TMath::Abs(particle->Y()) > 0.5) // NB: Use rapidity instead of pseudo rapidity!
			continue;

		Double_t r = TMath::Sqrt(particle->Xv() * particle->Xv() + particle->Yv() * particle->Yv());

		fSpectrums[code]->fPt->Fill(pt);
		fSpectrums[code]->fPtRadius->Fill(pt, r);

		Bool_t primary = IsPrimary(particle);
		if (code != kPi0)
		{
			fSpectrums[code]->fPtPrimaries[Int_t(primary)]->Fill(pt);
			continue;
		}


		// Reject MIPS and count again
		if (pt < 0.3)
			continue;

		if (primary)
			fPrimaryPi0[kGenerated]->FillS(pt);
		else
			fSecondaryPi0[kGenerated]->FillS(pt);

		AliAODMCParticle * parent = GetParent(i, flags.fMcParticles);

		if (!parent)
			continue;

		Int_t pcode = parent->GetPdgCode();

		fPi0Sources[Int_t(primary)]->Fill(pcode);
		
		if (primary)
		{
			fPrimaryPi0[kGenerated]->Fill(pcode, pt);
			continue;
		}

		// Only for decay pi0s
		//
		if (!IsPrimary(parent))
		{
			fSecondaryPi0[kGenerated]->Fill(pcode, pt);
			continue;
		}

		fFeedDownPi0[kGenerated]->FillAll(pcode, pt);
	}
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

	if (plabel <= -1)
		return 0;

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
void MesonSelectionMC::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// This method should be redefined here for 2 reasons:
	//    - There is no timing cut in MC
	//    - It allows to inspect MC clusters

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

		// TODO: Redefine Cluster Histogram?
		// There is no cluster histograms here
		// FillClusterHistograms(clus, eflags);
		// FillClusterMC(clus, eflags.fMcParticles);
	}

	if (candidates->GetEntriesFast() > 1 && !eflags.isMixing)
		fEventCounter->Fill(EventFlags::kTwoPhotons);
}