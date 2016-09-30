#include "TestPhotonSelection.h"


ClassImp(TestPhotonSelection);

TestPhotonSelection::TestPhotonSelection():
	PhotonSelection(), fEvents(0), fListOfHistos(0), fhPi0Mass() {}

//________________________________________________________________
TestPhotonSelection::TestPhotonSelection(const char * name, const char * title):
	PhotonSelection(name, title),
	fEvents(0),
	fListOfHistos(0),
	fhPi0Mass() {}

//________________________________________________________________
TestPhotonSelection::~TestPhotonSelection()
{
	delete fListOfHistos;
}

//________________________________________________________________
void TestPhotonSelection::InitSummaryHistograms()
{
	fEvents = new TH1F("TotalEvents", "Total number of analysed events", 1, 0, 1);
	fListOfHistos = new TList();
	// fListOfHistos->SetName("Data");
	fListOfHistos->SetOwner(kTRUE);
	fListOfHistos->Add(fEvents);
	// pi0 mass spectrum
	for (Int_t sm = 1; sm <  5; sm++)
	{
		fhPi0Mass[sm][sm] = new TH1F(Form("hPi0MassSM%iSM%i", sm, sm), "#pi^{0} mass spectrum", 250, 0, 0.5);
		fhPi0Mass[sm][sm]->SetXTitle("M_{#gamma#gamma}, GeV");
		fhPi0Mass[sm][sm]->SetYTitle("Counts");
		fListOfHistos->Add(fhPi0Mass[sm][sm]);
	}
}

//________________________________________________________________
void TestPhotonSelection::ConsiderPair(const AliVCluster * c1, const AliVCluster * c2, const EventFlags & eflags)
{
	TLorentzVector p1, p2, psum;
	c1->GetMomentum(p1, eflags.vtxBest);
	c2->GetMomentum(p2, eflags.vtxBest);
	psum = p1 + p2;

	// Pair cuts can be applied here
	if (psum.M2() < 0)  return;
	if (psum.Pt() < 2.) return;

	Int_t sm1, sm2;
	if ((sm1 = CheckClusterGetSM(c1)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2)) < 0) return; //  To be sure that everything is Ok

	Int_t s1 = (sm1 <= sm2) ? sm1 : sm2;
	Int_t s2 = (sm1 <= sm2) ? sm2 : sm1;

	if (fhPi0Mass[s1][s2])
		fhPi0Mass[s1][s2]->Fill(psum.M());
}

//________________________________________________________________
void TestPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime

	// Don't test mixed data
	if(eflags.isMixing)
		return;

	Double_t pi0EClusMin = 0.3;
	Int_t sm1;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->E() < pi0EClusMin) continue;
		if ((sm1 = CheckClusterGetSM(clus)) < 0) continue;
		candidates->Add(clus);
	}
}