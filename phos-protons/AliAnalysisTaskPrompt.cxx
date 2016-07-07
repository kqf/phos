#include "iostream"

// --- ROOT header files ---
#include <TFile.h>
#include <TObjArray.h>
#include <TROOT.h>

// --- AliRoot header files ---
#include "AliAnalysisTaskPrompt.h"
#include "AliAnalysisManager.h"
#include <AliVEvent.h>
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliVVertex.h>
#include <AliPHOSGeometry.h>
#include <AliLog.h>

// --- Custom libraries ---
#include "TestPhotonSelection.h"
#include "PhysPhotonSelection.h"



ClassImp(AliAnalysisTaskPrompt)

//________________________________________________________________
AliAnalysisTaskPrompt::AliAnalysisTaskPrompt() : AliAnalysisTaskSE(),
	fSelections(0),
	fPHOSBadMap(),
	fNBad(0),
	fBadCells(0)
{
	// Constructor for root I/O, do not use it
}

//________________________________________________________________
AliAnalysisTaskPrompt::AliAnalysisTaskPrompt(const char * name, Int_t nmodules) :
	AliAnalysisTaskSE(name),
	fSelections(new TList()),
	fPHOSBadMap(),
	fNBad(0),
	fBadCells(0)
{
	fSelections->SetOwner(kTRUE);
	fSelections->Add(new TestPhotonSelection("Data", "SOMETITLE")) ;
	fSelections->Add(new PhysPhotonSelection("Phys", "SOMETITLE")) ;
	for (int i = 0; i < fSelections->GetEntries(); ++i)
		DefineOutput(i + 1, TList::Class()); // Output starts from 1
}

//________________________________________________________________
AliAnalysisTaskPrompt::~AliAnalysisTaskPrompt()
{
	if (!AliAnalysisManager::GetAnalysisManager()->IsProofMode()) delete fSelections;
	if (fBadCells) delete [] fBadCells;
}

//________________________________________________________________
void AliAnalysisTaskPrompt::UserCreateOutputObjects()
{
	// Initialization of all outputs
	for (int i = 0; i < fSelections->GetEntries(); ++i)
	{
		PhotonSelection * fCellsQA = dynamic_cast<PhotonSelection *> (fSelections->At(i));
		fCellsQA->InitSummaryHistograms();
		PostData(i + 1, fCellsQA->GetListOfHistos()); // Output starts from 1
	}
}

//________________________________________________________________
void AliAnalysisTaskPrompt::UserExec(Option_t *)
{
	// Does the job for one event

	// event
	AliVEvent * event = InputEvent();
	if (!event)
	{
		AliWarning("Can't get event");
		return;
	}

	// check geometry
	if (!AliPHOSGeometry::GetInstance())
	{
		AliInfo("PHOS geometry not initialized, initializing it for you");
		AliPHOSGeometry::GetInstance("IHEP");
	}

	// Select Event
	EventFlags evtProperties;
	if (!EventSelected(event, evtProperties))
		return;


	// collect clusters (photon candidates)
	TObjArray clusArray;
	for (Int_t i = 0; i < event->GetNumberOfCaloClusters(); i++)
	{
		AliVCluster * clus = event->GetCaloCluster(i);
		if (!clus)
		{
			AliWarning("Can't get cluster");
			return;
		}

		// only basic filtering
		if (!clus->IsPHOS()) continue;
		if (IsClusterBad(clus)) continue;

		clusArray.Add(clus);
	}

	// No need to check. We have already done it in SelectEvent
	AliVCaloCells * cells = event->GetPHOSCells();


	for (int i = 0; i < fSelections->GetEntries(); ++i) // Fill and Post Data to outputs
	{
		PhotonSelection * fCellsQA = dynamic_cast<PhotonSelection *> (fSelections->At(i));

		if (!fCellsQA->SelectEvent(evtProperties))
			continue;

		fCellsQA->FillCellsInCluster(&clusArray, cells);
		fCellsQA->FillCells(cells);
		fCellsQA->FillPi0Mass(&clusArray, evtProperties);

		PostData(i + 1, fCellsQA->GetListOfHistos()); // Output starts from 1
	}
}

//________________________________________________________________
void AliAnalysisTaskPrompt::Terminate(Option_t *)
{
}

Bool_t AliAnalysisTaskPrompt::EventSelected(const AliVEvent * event, EventFlags & eprops) const
{
	// pileup
	if (event->IsPileupFromSPD(3, 0.8, 3., 2., 5.))
		return kFALSE;

	// cells
	AliVCaloCells * cells = event->GetPHOSCells();

	if (!cells)
	{
		AliWarning("Can't get cells");
		return kFALSE;
	}

	// primary vertex
	AliVVertex * vertex = (AliVVertex *) event->GetPrimaryVertex();
	if (!vertex)
	{
		AliWarning("Can't get primary vertex");
		return kFALSE;
	}

	vertex->GetXYZ(eprops.vtxBest);
	return kTRUE;
}

//____________________________________________________________
void AliAnalysisTaskPrompt::SetBadCells(Int_t badcells[], Int_t nbad)
{
	// Set absId numbers for bad cells;
	// clusters which contain a bad cell will be rejected.

	if (fBadCells) delete [] fBadCells;

	// switch off bad cells, if asked
	if (nbad <= 0)
	{
		fNBad = 0;
		return;
	}

	fNBad = nbad;
	fBadCells = new Int_t[nbad];

	for (Int_t i = 0; i < nbad; i++)
		fBadCells[i] = badcells[i];
}

//________________________________________________________________
Bool_t AliAnalysisTaskPrompt::CellInPhos(Int_t absId, Int_t & sm, Int_t & ix, Int_t & iz) const
{
	// Converts cell absId --> (sm,ix,iz);
	AliPHOSGeometry * geomPHOS = AliPHOSGeometry::GetInstance();
	if(!geomPHOS)
	{
		AliWarning("Something is wrong with PHOS Geometry. Check if you initialize it in UserExec!");
		return kTRUE;
	}

	Int_t relid[4];
	geomPHOS->AbsToRelNumbering(absId, relid);
	sm = relid[0];
	ix = relid[2];
	iz = relid[3];
	return (sm >= kMinModule) && (sm <= kMaxModule);
}

//________________________________________________________________
Bool_t AliAnalysisTaskPrompt::IsClusterBad(AliVCluster * clus) const
{
	// Returns true if cluster contains a bad cell
	for (Int_t b = 0; b < fNBad; b++)
		for (Int_t c = 0; c < clus->GetNCells(); c++)
			if (clus->GetCellAbsId(c) == fBadCells[b])
				return kTRUE;

	// If fBadCells array is empty then use BadMap

	if( !fPHOSBadMap[0] ) return kFALSE;

	Int_t sm, ix, iz;
	for (Int_t c = 0; c < clus->GetNCells(); c++) // Loop over all cells in cluster
	{
		if(!CellInPhos(clus->GetCellAbsId(c), sm, ix, iz)) // Reject cells outside PHOS
			return kTRUE;

		if (!fPHOSBadMap[sm - kMinModule]) // Warn if something is wrong
			AliError(Form("No Bad map for PHOS module %d", sm));

		if (fPHOSBadMap[sm - kMinModule]->GetBinContent(ix, iz) > 0) // Check if cell is bad
			return kTRUE;

	}

	return kFALSE;
}
void AliAnalysisTaskPrompt::SetBadMap(const char * filename)
{
	TFile * fBadMap = TFile::Open(filename);
	if (!fBadMap->IsOpen())
		AliFatal(Form("Cannot set BadMap %s doesn't exist", filename));

	cout << "\n\n...Adding PHOS bad channel map \n"  << endl;
	gROOT->cd();

	for (Int_t module = kMinModule; module <= kMaxModule; ++module)
	{
		TH2I * h = (TH2I *) fBadMap->Get(Form("PHOS_BadMap_mod%d", module));
		if (!h) AliFatal( Form("PHOS_BadMap_mod%d doesn't exist", module));

		fPHOSBadMap[module - kMinModule] = new TH2I(*h);
		cout << "Set " <<  fPHOSBadMap[module - kMinModule]->GetName() << endl;
	}
	fBadMap->Close();
	cout << "\n\n...PHOS BadMap is set now." << endl;
}