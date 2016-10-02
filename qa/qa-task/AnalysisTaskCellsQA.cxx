#include <TFile.h>
#include <TObjArray.h>

#include <AnalysisTaskCellsQA.h>
#include "AliAnalysisManager.h"
#include <AliVEvent.h>
#include <AliVCaloCells.h>
#include <AliVCluster.h>
#include <AliVVertex.h>
#include <AliEMCALGeometry.h>
#include <AliPHOSGeometry.h>
#include <AliLog.h>

ClassImp(AnalysisTaskCellsQA)

//________________________________________________________________
AnalysisTaskCellsQA::AnalysisTaskCellsQA() : AliAnalysisTaskSE("CellsQA"),
  fOutput(0)
{
  // Constructor for root I/O, do not use it
  DefineOutput(1, TList::Class());
}


//________________________________________________________________
AnalysisTaskCellsQA::~AnalysisTaskCellsQA()
{
  // if (!AliAnalysisManager::GetAnalysisManager()->IsProofMode()) delete fCellsQA;
}

//________________________________________________________________
void AnalysisTaskCellsQA::UserCreateOutputObjects()
{
  // Per run histograms cannot be initialized here

  fOutput = new TList();
  fOutput->SetOwner(kTRUE);
  for (int j = 0; j < 10; ++j)
  {
    int i = 30 * j + 2 * j;
    fOutput->Add(new TH1F(Form("hCellEnergy_%d", i), Form("Energy for cell #%d ; Amplitude [GeV]", i), 1000, 0, 1) );
  }
  PostData(1, fOutput);
}

//________________________________________________________________
void AnalysisTaskCellsQA::UserExec(Option_t *)
{
  // Does the job for one event

  // event
  AliVEvent * event = InputEvent();
  if (!event)
  {
    AliWarning("Could not get event");
    return;
  }

  else
  {
    if (!AliPHOSGeometry::GetInstance())
    {
      AliInfo("PHOS geometry not initialized, initializing it for you");
      AliPHOSGeometry::GetInstance("IHEP");
    }
  }

  // pileup;  FIXME: why AliVEvent does not allow a version without arguments?
  if (event->IsPileupFromSPD(3, 0.8, 3., 2., 5.))
    return;

  // cells
  AliVCaloCells * cells = event->GetPHOSCells();

  if (!cells)
  {
    AliWarning("Could not get cells");
    return;
  }

  // primary vertex
  AliVVertex * vertex = (AliVVertex *) event->GetPrimaryVertex();
  if (!vertex)
  {
    AliWarning("Could not get primary vertex");
    return;
  }


  // Fill cell histograms not related with a cluster

  Short_t absId;
  Int_t mclabel;
  Double_t amp, time, efrac;
  Int_t sm;

  for (Short_t c = 0; c < cells->GetNumberOfCells(); c++)
  {
    cells->GetCell(c, absId, amp, time, mclabel, efrac);
    if ((sm = GetSM(absId)) < 0) continue;
    FillHistogram(Form("hCellEnergy_%d", absId), amp);

  } // cell loop


  PostData(1, fOutput);
}

//________________________________________________________________
void AnalysisTaskCellsQA::Terminate(Option_t *)
{
}

//_____________________________________________________________________________
void AnalysisTaskCellsQA::FillHistogram(const char * key, Double_t x, Double_t y)const
{
  //FillHistogram
  TH1 * th1 = dynamic_cast<TH1 *> (fOutput->FindObject(key));
  if (th1)
    th1->Fill(x, y) ;
  else
    AliError(Form("can not find histogram (of instance TH1) <%s> ", key)) ;
}

Int_t AnalysisTaskCellsQA::GetSM(Int_t absId)
{
  Int_t sm = 1 + (absId - 1) / 3584;

  // check for data corruption to avoid segfaults
  if (sm < 0 || sm > 9)
  {
    AliError("Data corrupted");
    return -1;
  }

  return sm;
}
