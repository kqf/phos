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
	fListOfHistos->SetOwner(kTRUE);
	fListOfHistos->Add(fEvents);
	// pi0 mass spectrum

	TH1F * hist = new TH1F("hPi0Mass", "Invariant mass sectrum for #pi^{0} extraction, %s", 250, 0, 0.5);
	hist->SetXTitle("M_{#gamma#gamma}, GeV");
	hist->SetYTitle("Counts");

	fhPi0Mass = DetectorHistogram(hist, fListOfHistos);
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

	Int_t sm1, sm2, x, z; // x, z are unused here 
	if ((sm1 = CheckClusterGetSM(c1, x, z)) < 0) return; //  To be sure that everything is Ok
	if ((sm2 = CheckClusterGetSM(c2, x, z)) < 0) return; //  To be sure that everything is Ok

	Int_t s1 = (sm1 <= sm2) ? sm1 : sm2;
	Int_t s2 = (sm1 <= sm2) ? sm2 : sm1;

	if (sm1 == sm2)
		fhPi0Mass.FillAll(sm1, psum.M());
}

//________________________________________________________________
void TestPhotonSelection::SelectPhotonCandidates(const TObjArray * clusArray, TObjArray * candidates, const EventFlags & eflags)
{
	// Don't return TObjArray: force user to handle candidates lifetime

	// Don't test mixed data
	if(eflags.isMixing)
		return;

	Double_t pi0EClusMin = 0.3;
	Int_t sm1, x, z;
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->E() < pi0EClusMin) continue;
		if ((sm1 = CheckClusterGetSM(clus, x, z)) < 0) continue;
		candidates->Add(clus);
	}
}