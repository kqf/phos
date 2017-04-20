
#include <AliAnalysisTaskCaloCellsQA.h>
#include <AliCaloCellsQA.h>
#include <AliAnalysisManager.h>
#include <AliInputEventHandler.h>

#include "iostream"

class AliCaloCellsQAPt: public AliCaloCellsQA
{
public:
	AliCaloCellsQAPt(): AliCaloCellsQA(), mPairPtCut(1), fhNAllEventsProcessedPerRun(0) {} // Required for reading
	AliCaloCellsQAPt(Int_t nmods, Int_t det = kPHOS, Int_t startRunNumber = 100000, Int_t endRunNumber = 300000):
		AliCaloCellsQA(nmods, det, startRunNumber, endRunNumber), mPairPtCut(1), fhNAllEventsProcessedPerRun(0) {}
	virtual void FillPi0Mass(TObjArray * clusArray, Double_t vertexXYZ[3]);
	void SetPairPtCut(Double_t c) { mPairPtCut = c; }
	virtual void InitSummaryHistograms(Int_t nbins = 400, Double_t emax = 4.,
	                                   Int_t nbinsh = 100, Double_t emaxh = 300.,
	                                   Int_t nbinst = 250, Double_t tmin = -0.1e-6, Double_t tmax = 0.15e-6)
	{
		AliCaloCellsQA::InitSummaryHistograms(nbins, emax, nbinsh, emaxh, nbinst, tmin, tmax);
		fhNAllEventsProcessedPerRun = dynamic_cast<TH1D *>(fhNEventsProcessedPerRun->Clone("hNEventsProcessedPerRun"));
		fhNAllEventsProcessedPerRun->SetTitle("Number of all events vs run number");
	}


protected:
	Int_t CheckClusterGetSM(AliVCluster * clus)
	{
		// Reject CPV clusters (new in luster
		if (clus->GetType() != AliVCluster::kPHOSNeutral) return -1;
		if (clus->GetNCells() < 3) return -1;
		if (clus->E() < 0.3) return -1;

		// Float_t timesigma = 12.5e-9;
		// if (TMath::Abs(clus->GetTOF()) > timesigma) return -1;

		return AliCaloCellsQA::CheckClusterGetSM(clus);
	}

	Double_t mPairPtCut;

public:
	TH1D *fhNAllEventsProcessedPerRun; //! This counts all events processed in the run

private:
	ClassDef(AliCaloCellsQAPt, 2);
};



class AliAnalysisTaskCaloCellsQAPt: public AliAnalysisTaskCaloCellsQA
{
public:
	AliAnalysisTaskCaloCellsQAPt(): AliAnalysisTaskCaloCellsQA() {}
	AliAnalysisTaskCaloCellsQAPt(const char * name, Int_t nmods = 10, Int_t det = AliAnalysisTaskCaloCellsQA::kPHOS, char * outfile = 0):
		AliAnalysisTaskCaloCellsQA(name, nmods, det, outfile)
	{
		if (fCellsQA) delete fCellsQA;
		fCellsQA = new AliCaloCellsQAPt(nmods, AliCaloCellsQA::kPHOS);

		// if (outfile)
		// fOutfile = outfile;
		// else
		// DefineOutput(1, TObjArray::Class());

	}

	void CollisionCandidate(UInt_t mask)
	{
		fTriggerMask = mask;
	}

	void UserExec(Option_t * opt)
	{
		// This is needed to check total number of events
		Bool_t isSelected = (((AliInputEventHandler*)(AliAnalysisManager::GetAnalysisManager()->GetInputEventHandler()))->IsEventSelected() & AliVEvent::kMB);


		AliVEvent * event = InputEvent();
		if (!event)
			return;

		AliCaloCellsQAPt * qaPt = dynamic_cast<AliCaloCellsQAPt *>(fCellsQA);

		if (qaPt)
			qaPt->fhNAllEventsProcessedPerRun->Fill(event->GetRunNumber());

		if (!isSelected)
			return;

		AliVVertex * vertex = (AliVVertex *) event->GetPrimaryVertex();
		if (!vertex) return;

		if (TMath::Abs(vertex->GetZ()) > 10) return;

		AliAnalysisTaskCaloCellsQA::UserExec(opt);
	}


	void SetPairPtCut(Double_t cut)
	{
		AliCaloCellsQAPt * cqa = dynamic_cast<AliCaloCellsQAPt * >(fCellsQA);
		if (!cqa) cout << "ERROR ERROR ERROR" << endl;

		cqa->SetPairPtCut(cut);
	}
protected:
	UInt_t fTriggerMask;
	ClassDef(AliAnalysisTaskCaloCellsQAPt, 2);
};

void AliCaloCellsQAPt::FillPi0Mass(TObjArray * clusArray, Double_t vertexXYZ[3])
{
	// Fill gamma+gamma invariant mass histograms.
	// ri -- run index.

	Int_t sm1, sm2;
	TLorentzVector p1, p2, psum;

	// cluster loop
	for (Int_t i = 0; i < clusArray->GetEntriesFast(); i++)
	{
		AliVCluster * clus = (AliVCluster *) clusArray->At(i);
		if (clus->E() < fPi0EClusMin) continue;
		if ((sm1 = CheckClusterGetSM(clus)) < 0) continue;
		if (clus->GetNCells() < 3) continue;

		clus->GetMomentum(p1, vertexXYZ);

		// second cluster loop
		for (Int_t j = i + 1; j < clusArray->GetEntriesFast(); j++)
		{
			AliVCluster * clus2 = (AliVCluster *) clusArray->At(j);
			if (clus2->E() < fPi0EClusMin) continue;
			if ((sm2 = CheckClusterGetSM(clus2)) < 0) continue;
			if (clus2->GetNCells() < 3) continue;

			clus2->GetMomentum(p2, vertexXYZ);

			psum = p1 + p2;
			if (  psum.M2() < 0 ) continue;
			if (  psum.Pt() < mPairPtCut ) continue;

			// s1 <= s2
			Int_t s1 = (sm1 <= sm2) ? sm1 : sm2;
			Int_t s2 = (sm1 <= sm2) ? sm2 : sm1;

			if (fhPi0Mass[s1][s2])
				fhPi0Mass[s1][s2]->Fill(psum.M());
		} // second cluster loop
	} // cluster loop
}
