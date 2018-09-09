#ifndef ALIANALYSISTASKPHOSTRIGGERQAV1_CXX
#define ALIANALYSISTASKPHOSTRIGGERQAV1_CXX

/* Copyright(c) 1998-1999, ALICE Experiment at CERN, All rights reserved. *
 * See cxx source for full Copyright notice     */

// QA of PHOS Trigger data.
// Author: Boris Polishchuk

#include "AliAnalysisTaskSE.h"

class AliPHOSGeometry;
class AliESDCaloCells;
class AliESDCaloCluster;

class AliAnalysisTaskPHOSTriggerQAv1 : public AliAnalysisTaskSE {

public:

  AliAnalysisTaskPHOSTriggerQAv1();
  AliAnalysisTaskPHOSTriggerQAv1(const char *name, Int_t L1_threshold=-1);
  virtual ~AliAnalysisTaskPHOSTriggerQAv1() {}
  
  virtual void   UserCreateOutputObjects();
  virtual void   UserExec(Option_t *option);

  void SelectL1Threshold(Int_t L1_threshold) { fL1Threshold = L1_threshold; } 
  
private:

  AliAnalysisTaskPHOSTriggerQAv1(const AliAnalysisTaskPHOSTriggerQAv1&); // not implemented
  AliAnalysisTaskPHOSTriggerQAv1& operator=(const AliAnalysisTaskPHOSTriggerQAv1&); // not implemented

  void FillHistogram(const char * key,Double_t x) const ; //Fill 1D histogram witn name key
  void FillHistogram(const char * key,Double_t x, Double_t y) const ; //Fill 2D histogram witn name key

  void   MaxEnergyCellPos(AliVCaloCells *cells, AliVCluster* clu, Int_t& maxId);
  Bool_t Matched(Int_t *trig_relid,Int_t *cluster_relid); //is cluster position coincides with 4x4 position?

  Int_t GetTRUNum(Int_t cellX, Int_t cellZ);

private:

  TList * fOutputContainer;   //final histogram container
  Int_t fEventCounter;        // number of analyzed events
  Int_t fL1Threshold;         // -1 - L0, 0 - L1 High, 1 - L1 Medium, 2 - L1 Low

  ClassDef(AliAnalysisTaskPHOSTriggerQAv1, 1); // PHOS analysis task
};

#endif