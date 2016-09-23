
#include <AliAnalysisTaskCaloCellsQA.h>
#include <AliCaloCellsQA.h>

#include "iostream"

class AliCaloCellsQAPt: public AliCaloCellsQA
{
public:
	AliCaloCellsQAPt(): AliCaloCellsQA(), mPairPtCut(1) {} // Required for reading
	AliCaloCellsQAPt(Int_t nmods, Int_t det = kPHOS, Int_t startRunNumber = 100000, Int_t endRunNumber = 300000):
		AliCaloCellsQA(nmods, det, startRunNumber, endRunNumber), mPairPtCut(1) {}
	virtual void FillPi0Mass(TObjArray * clusArray, Double_t vertexXYZ[3]);
	void SetPairPtCut(Double_t c) { mPairPtCut = c; }

protected:
	Int_t CheckClusterGetSM(AliVCluster * clus)
	{
		// Reject CPV clusters (new in luster
		if (clus->GetType() != AliVCluster::kPHOSNeutral) return -1;
		return AliCaloCellsQA::CheckClusterGetSM(clus);
	}

	Double_t mPairPtCut;
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
	void SetPairPtCut(Double_t cut)
	{
		AliCaloCellsQAPt * cqa = dynamic_cast<AliCaloCellsQAPt * >(fCellsQA);
		if (!cqa) cout << "ERROR ERROR ERROR" << endl;

		cqa->SetPairPtCut(cut);
	}
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
