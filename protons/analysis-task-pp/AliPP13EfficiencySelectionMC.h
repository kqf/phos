#ifndef ALIPP13EFFICIENCYSELECTIONMC_H
#define ALIPP13EFFICIENCYSELECTIONMC_H


#include <map>

// --- Custom header files ---
#include "AliPP13PhotonSelection.h"
#include "AliPP13SelectionWeights.h"
#include "AliPP13MesonSelectionMC.h"

// --- ROOT system ---
#include <TClonesArray.h>
#include <TObjArray.h>
#include <TList.h>
#include <TF1.h>

// --- AliRoot header files ---
#include <AliAODMCParticle.h>
#include <AliVCluster.h>
#include <AliStack.h>
#include <AliLog.h>


// NB: This will simplify the code
//


// struct ParticleSpectrum
// {
// 	ParticleSpectrum(const char * n, TList * fListOfHistos, Int_t ptsize, Float_t * ptbins, Bool_t full = kTRUE):
// 		fPtAllRange(0),
// 		fPtRadius(0),
// 		fEtaPhi(0),
// 		fPtLong(0),
// 		fPt(0),
// 		fPtPrimaries()
// 	{
// 		fPtAllRange = new TH1F(Form("hPt_allrange_%s", n), Form("Generated p_{T} spectrum of %ss in 4 #pi ; p_{T}, GeV/c", n), ptsize, ptbins);
// 		fPtRadius   = new TH2F(Form("hPt_%s_radius", n), Form("Generated radius, p_{T} spectrum of all %ss; r, cm; p_{T}, GeV/c", n), 500, 0., 500., 400, 0, 20);
// 		fEtaPhi     = new TH2F(Form("hEtaPhi_%s", n), Form("Generated %ss y vs #phi plot; #phi (rad); y", n), 100, 0, TMath::Pi() * 2, 100, -1, 1);
// 		fPtLong     = new TH1F(Form("hPtLong_%s", n), Form("Generated p_{T} spectrum of %ss; p_{T}, GeV/c", n), 1000, 0, 100);
// 		fPt         = new TH1F(Form("hPt_%s", n), Form("Generated p_{T} spectrum of %ss; p_{T}, GeV/c", n), ptsize, ptbins);

// 		fListOfHistos->Add(fPtAllRange);
// 		fListOfHistos->Add(fPtRadius);
// 		fListOfHistos->Add(fEtaPhi);
// 		fListOfHistos->Add(fPtLong);
// 		fListOfHistos->Add(fPt);

// 		if (!full)
// 			return;

// 		for(Int_t i = 0; i < 2; ++i)
// 		{
// 			const char * s = (i == 0) ? "secondary": "primary";
// 			fPtPrimaries[i] = new TH1F(Form("hPt_%s_%s_", n, s), Form("Generated p_{T} spectrum of %s %ss; p_{T}, GeV/c", s, n), ptsize, ptbins);
// 			fListOfHistos->Add(fPtPrimaries[i]);
// 		}
// 	}

// // private:

// 	TH1F * fPtAllRange; //!
// 	TH2F * fPtRadius;   //!
// 	TH2F * fEtaPhi;     //!
// 	TH1F * fPtLong;     //!
// 	TH1F * fPt;         //!
// 	TH1F * fPtPrimaries[2]; //!

// };


class AliPP13EfficiencySelectionMC: public AliPP13PhotonSelection
{
public:
	enum Particles
	{
		kGamma = 22, kPi0 = 111, kEta = 221, kK0s = 310
	};

				
	AliPP13EfficiencySelectionMC():
		AliPP13PhotonSelection(),
		fWeights(),
		fInvMass()
	{
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";
	}

	AliPP13EfficiencySelectionMC(const char * name, const char * title, AliPP13ClusterCuts cuts, AliPP13SelectionWeights w):
		AliPP13PhotonSelection(name, title, cuts),
		fWeights(w),
		fInvMass()
	{
		// Force no timing cut for MC,
		// as there is no photons from different bunches
		fCuts.fTimingCut = 9999; 

		// Don't use c++11 here, as it might fail at some nodes
		fPartNames[kGamma] = "#gamma";
		fPartNames[kPi0] = "#pi^{0}";
		fPartNames[kEta] = "#eta";

	}

	virtual void InitSelectionHistograms();
	virtual void ConsiderGeneratedParticles(const EventFlags & eflags);

	virtual ~AliPP13EfficiencySelectionMC()
	{
		for (ParticleSpectrums::iterator i = fSpectrums.begin(); i != fSpectrums.end(); ++i)
			delete i->second;
	}

protected:
	virtual void ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags);
	virtual Bool_t IsPrimary(const AliAODMCParticle * particle) const;

	// NB: Impelement these methods if needed
	// 
	void ConsiderGeneratedParticle(Int_t i, Double_t pt, Bool_t primary, const EventFlags & flags) 
	{
		(void) i;
		(void) pt;
		(void) primary;
		(void) flags;

	}

	void ConsiderReconstructedParticle(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
	{
		(void) c1;
		(void) c2;
		(void) eflags;
	}


	AliPP13EfficiencySelectionMC(const AliPP13EfficiencySelectionMC &);
	AliPP13EfficiencySelectionMC & operator = (const AliPP13EfficiencySelectionMC &);

	AliPP13SelectionWeights fWeights;

	// NB: This data structure contains all necesary histograms
	//     for the particles we want to get
	typedef std::map<Int_t, ParticleSpectrum * > ParticleSpectrums;
	ParticleSpectrums fSpectrums;

	typedef std::map<Int_t, TString> EnumNames;
	EnumNames fPartNames;

	TH1 * fInvMass[2]; //!
	ClassDef(AliPP13EfficiencySelectionMC, 2)
};
#endif