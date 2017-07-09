// --- Custom header files ---
#include "PythiaInfoSelection.h"

// --- ROOT system ---
#include <TProfile.h>
#include <TSystem.h>
#include <TFile.h>
#include <TTree.h>
#include <TKey.h>

// --- AliRoot header files ---
#include <AliLog.h>
#include <AliAnalysisManager.h>

#include <iostream>
using namespace std;


ClassImp(PythiaInfoSelection);

//________________________________________________________________
void PythiaInfoSelection::CountMBEvent()
{
	
	GeneralPhotonSelection::CountMBEvent();

	// Fetch the histgram file
	TTree * tree = AliAnalysisManager::GetAnalysisManager()->GetTree();

	if (!tree)
	{
		// AliError(Form("%s - UserNotify: No current tree!", GetName()));
		return;
	}

	TFile * curfile = tree->GetCurrentFile();
	if (!curfile)
	{
		// AliError(Form("%s - UserNotify: No current file!", GetName()));
		return;
	}

	TString file(curfile->GetName());
	file.ReplaceAll(gSystem->BaseName(file.Data()), "");

	TFile fxsec(Form("%s%s", file.Data(), "pyxsec_hists.root"));

	if (!fxsec.IsOpen())
	{
		// AliError(Form("There is no pyxsec_hists.root in this directory."));
		return;
	}

	// find the tlist we want to be independtent of the name so use the Tkey
	TKey * key = (TKey *)fxsec.GetListOfKeys()->At(0);
	if (!key)
		return;

	TList * list = dynamic_cast<TList *>(key->ReadObj());
	if (!list)
		return;

	Float_t xsec    = ((TProfile *)list->FindObject("h1Xsec"))  ->GetBinContent(1);
	Float_t trials  = ((TH1F *)    list->FindObject("h1Trials"))->GetBinContent(1);

	if(fxsec.IsOpen())
		fxsec.Close();

	FillHistogram("hXsec", 0.5, xsec);
	FillHistogram("hTrials", 0.5, trials);
}

//________________________________________________________________
void PythiaInfoSelection::FillPi0Mass(TClonesArray * clusArray, TList * pool, const EventFlags & eflags)
{
	(void) clusArray;
	(void) pool;
	(void) eflags;

}


//________________________________________________________________
void PythiaInfoSelection::ConsiderGeneratedParticles(TClonesArray * particles, TClonesArray * clusArray, const EventFlags & eflags)
{
	(void) particles;
	(void) clusArray;
	(void) eflags;
}


//________________________________________________________________
void PythiaInfoSelection::InitSelectionHistograms()
{

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
}


