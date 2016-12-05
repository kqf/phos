#ifndef AliAnalysisTaskPi0v4_cxx
#define AliAnalysisTaskPi0v4_cxx

/* Copyright(c) 1998-1999, ALICE Experiment at CERN, All rights reserved. *
 * See cxx source for full Copyright notice     */

// Analysis task for pi0 and eta meson analysis in pp collisions in AOD
// Authors: Yuri Kharlov, Dmitri Peressounko

#include "TROOT.h"
#include "TFile.h"

class TObjArray;
class TList;
class TClonesArray;
class TH1F;
class TH2I;
class TH2F;
class TH3F;
class AliPHOSGeometry;
class TFile;
// class AliTriggerAnalysis;

#include "TH2I.h"
#include "AliAnalysisTaskSE.h"
#include "AliLog.h"

class AliAnalysisTaskPi0v4 : public AliAnalysisTaskSE {
public:
  AliAnalysisTaskPi0v4(const char *name = "AliAnalysisTaskPi0v4");
  virtual ~AliAnalysisTaskPi0v4() {}
  
  virtual void   UserCreateOutputObjects();
  virtual void   UserExec(Option_t *option);
  virtual void   Terminate(Option_t *);
  void SetBCgap(const Double_t bcgap) {fBCgap = bcgap;}
  void SetSelectTriggerClass(const char *trigClass) {fSelectTrigClass = trigClass;}
  void SetRecalib(const Int_t mod, const Double_t recalib)
  {
    if (mod<1 || mod>5) AliFatal(Form("Wrong module number: %d",mod));
    else fRecalib[mod-1] = recalib;
  }
  void SetPHOSBadMap(Int_t mod,TH2I * h)
  {
    if(fPHOSBadMap[mod]) delete fPHOSBadMap[mod] ;
    fPHOSBadMap[mod]=new TH2I(*h) ;
    printf("Set %s \n",fPHOSBadMap[mod]->GetName());
  }

  void SetBadMap(const char * filename)
  {
    return;
    TFile * fBadMap = TFile::Open(filename, "read");
    if (!fBadMap->IsOpen())
    {
     cout << Form("Cannot set BadMap %s doesn't exist", filename) << endl;
     return;
    }
      // AliFatal(Form("Cannot set BadMap %s doesn't exist", filename));

    cout << "\n\n...Adding PHOS bad channel map \n"  << endl;
    gROOT->cd();

    for (Int_t module = 1; module <= 4; ++module)
    {
      TH2I * h = (TH2I *) fBadMap->Get(Form("PHOS_BadMap_mod%d", module));
      if (!h) AliFatal( Form("PHOS_BadMap_mod%d doesn't exist", module));

      fPHOSBadMap[module] = new TH2I(*h);
      cout << "Set " <<  fPHOSBadMap[module]->GetName() << endl;
    }
    fBadMap->Close();
    cout << "\n\n...PHOS BadMap is set now." << endl;
  }

  
private:
  AliAnalysisTaskPi0v4(const AliAnalysisTaskPi0v4&); // not implemented
  AliAnalysisTaskPi0v4& operator=(const AliAnalysisTaskPi0v4&); // not implemented
  Bool_t IsGoodChannel(const char * det, Int_t mod,Int_t ix, Int_t iz);
  void FillHistogram(const char * key,Double_t x) const ; //Fill 1D histogram witn name key
  void FillHistogram(const char * key,Double_t x, Double_t y) const ; //Fill 2D histogram witn name key
  void FillHistogram(const char * key,Double_t x, Double_t y, Double_t z) const ; //Fill 3D histogram witn name key
  Bool_t TestLambda(Double_t l1,Double_t l2) ;
  Int_t  TestBC(Double_t tof) ;
 
private:
  TList * fOutputContainer;       //final histogram container
  TList * fPHOSEvents[10][2] ;    //Container for PHOS photons
  TClonesArray * fPHOSEvent ;     //PHOS photons in current event
  TString fSelectTrigClass;  // Trigger class name to select in analysis
  
  Double_t fBCgap;          // time gap between BC in seconds
  Double_t fRecalib[5];     // Correction for abs.calibration per module

  TH2I *fPHOSBadMap[6] ;    //Container for PHOS bad channels map

  AliPHOSGeometry  *fPHOSGeo;  // PHOS geometry
  Int_t fEventCounter;         // number of analyzed events
  // AliTriggerAnalysis *fTriggerAnalysis; //! Trigger Analysis for Normalisation

  ClassDef(AliAnalysisTaskPi0v4, 1); // PHOS analysis task
};

#endif
