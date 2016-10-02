#ifndef ANALYSISTASKCELLSQA_H
#define ANALYSISTASKCELLSQA_H

#include <TString.h>

#include <AliAnalysisTaskSE.h>
#include <AliCaloCellsQA.h>

class AnalysisTaskCellsQA : public AliAnalysisTaskSE {

public:


  AnalysisTaskCellsQA();
  virtual ~AnalysisTaskCellsQA();

  void   UserCreateOutputObjects();
  void   UserExec(Option_t *);
  void   Terminate(Option_t *);

  void FillHistogram(const char * key,Double_t x, Double_t y = 1.) const;

private:
  Int_t GetSM(Int_t absId);
  AnalysisTaskCellsQA(const AnalysisTaskCellsQA &);
  AnalysisTaskCellsQA & operator = (const AnalysisTaskCellsQA &);

private:
  TList * fOutput;                //< List of histograms for data

  ClassDef(AnalysisTaskCellsQA, 2);
};

#endif
