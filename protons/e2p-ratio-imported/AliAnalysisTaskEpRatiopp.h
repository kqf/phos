#ifndef AliAnalysisTaskEpRatiopp_cxx
#define AliAnalysisTaskEpRatiopp_cxx

// E/p analysis task.
// Authors: Boris Polishchuk, Tsubasa Okubo

class AliPHOSGeometry;
class AliAnalysisTaskSE;
class AliPIDResponse;
#include "AliLog.h"
#include "AliAnalysisTaskSE.h"

class AliAnalysisTaskEpRatiopp : public AliAnalysisTaskSE {

public:
  AliAnalysisTaskEpRatiopp(const char *name = "AliAnalysisTaskEpRatiopp");
  virtual ~AliAnalysisTaskEpRatiopp() {}
  
  virtual void   UserCreateOutputObjects();
  virtual void   UserExec(Option_t *option);
  void SetRecalib(const Int_t mod, const Double_t recalib)
  {
    if (mod<1 || mod>5) AliFatal(Form("Wrong module number: %d",mod));
    else fRecalib[mod-1] = recalib;
  }
  
private:
  AliAnalysisTaskEpRatiopp(const AliAnalysisTaskEpRatiopp&); // not implemented
  AliAnalysisTaskEpRatiopp& operator=(const AliAnalysisTaskEpRatiopp&); // not implemented

  void SetGeometry();
  void FillHistogram(const char * key,Double_t x) const ; //Fill 1D histogram witn name key
  void FillHistogram(const char * key,Double_t x, Double_t y) const ; //Fill 2D histogram witn name key
  void FillHistogram(const char * key,Double_t x, Double_t y, Double_t z) const ; //Fill 3D histogram witn name key
  
private:

  Int_t fRunNumber;
  TList * fOutputContainer;     // final histogram container
  AliPHOSGeometry  *fPHOSGeo;   // PHOS geometry
  AliPIDResponse *fPIDResponse; // PID Response
  Double_t fRecalib[5];     // Correction for abs.calibration per module

  ClassDef(AliAnalysisTaskEpRatiopp, 1); // PHOS analysis task
};

#endif
