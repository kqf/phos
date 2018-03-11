#include <AliAnalysisTaskCaloCellsPhysQA.h>
#include <AliCaloCellsPhysQA.h>

ClassImp(AliAnalysisTaskCaloCellsPhysQA);

//________________________________________________________________
void AliAnalysisTaskCaloCellsPhysQA::AliAnalysisTaskCaloCellsPhysQA(
	const char * name, Int_t nmods = 10, Int_t det = AliAnalysisTaskCaloCellsQA::kPHOS, char * outfile = 0
):
	AliAnalysisTaskCaloCellsQA(name, nmods, det, outfile)

{
	// NB: Override the original QA analysis
	//
	if (fCellsQA)
	{
		delete fCellsQA;
		fCellsQA = 0;
	}

	fCellsQA = new AliCaloCellsPhysQA(nmods, AliCaloCellsQA::kPHOS);
}
