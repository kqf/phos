/**************************************************************************
 * Copyright(c) 1998-1999, ALICE Experiment at CERN, All rights reserved. *
 *                                                                        *
 * Author: The ALICE Off-line Project.                                    *
 * Contributors are mentioned in the code where appropriate.              *
 *                                                                        *
 * Permission to use, copy, modify and distribute this software and its   *
 * documentation strictly for non-commercial purposes is hereby granted   *
 * without fee, provided that the above copyright notice appears in all   *
 * copies and that both the copyright notice and this permission notice   *
 * appear in the supporting documentation. The authors make no claims     *
 * about the suitability of this software for any purpose. It is          *
 * provided "as is" without express or implied warranty.                  *
 **************************************************************************/

// Analysis task for pi0 and eta meson analysis in pp collisions in AOD
// Authors: Yuri Kharlov, Dmitri Peressounko

#include "TChain.h"
#include "TTree.h"
#include "TObjArray.h"
#include "TClonesArray.h"
#include "TF1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH2I.h"
#include "TH3F.h"
#include "TParticle.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "THashList.h"

#include "AliInputEventHandler.h"
#include "AliAnalysisManager.h"
#include "AliAnalysisTaskSE.h"
#include "AliAnalysisTaskPi0v4.h"
#include "AliCaloPhoton.h"
#include "AliPHOSGeometry.h"
#include "AliAODEvent.h"
#include "AliESDEvent.h"
#include "AliVCaloCells.h"
#include "AliVCluster.h"
#include "AliVVertex.h"
#include "AliLog.h"
#include "AliPID.h"
#include "AliOADBContainer.h"
// #include "AliTriggerAnalysis.h"

// Analysis task to fill histograms with PHOS clusters and cells
// Authors: Yuri Kharlov
// Date   : 28.05.2009

ClassImp(AliAnalysisTaskPi0v4)

//________________________________________________________________________
AliAnalysisTaskPi0v4::AliAnalysisTaskPi0v4(const char * name)
  : AliAnalysisTaskSE(name),
    fOutputContainer(0),
    fPHOSEvent(0),
    fSelectTrigClass(""),
    fBCgap(525e-09),
    fPHOSGeo(0),
    fEventCounter(0)
{
  // Constructor
  Int_t nBin = 10 ;
  for (Int_t i = 0; i < nBin; i++)
  {
    for (Int_t j = 0; j < 2; j++)
      fPHOSEvents[i][j] = 0 ;
  }

  // Output slots #0 write into a TH1 container
  DefineOutput(1, TList::Class());

  // Set bad channel map
  char key[55] ;
  for (Int_t i = 0; i < 6; i++)
  {
    snprintf(key, 55, "PHOS_BadMap_mod%d", i) ;
    fPHOSBadMap[i] = new TH2I(key, "Bad Modules map", 64, 0., 64., 56, 0., 56.) ;
  }

  // Absolute recalibration for LHC11a. Use SetRecalib(mod,recalib) to change it
  fRecalib[0] = 0.9942;
  fRecalib[1] = 0.9822;
  fRecalib[2] = 1.0072;
  fRecalib[3] = 1.0000;

}

//________________________________________________________________________
void AliAnalysisTaskPi0v4::UserCreateOutputObjects()
{
  // Create histograms
  // Called once

  // AOD histograms
  if (fOutputContainer != NULL)
    delete fOutputContainer;
  fOutputContainer = new THashList();
  fOutputContainer->SetOwner(kTRUE);

  fOutputContainer->Add(new TH1F("hSelEvents", "Selected events", 8, -0.5, 7.5));
  fOutputContainer->Add(new TH2F("hClusterEvsN", "Cluster energy vs digit multiplicity", 1000, 0., 200., 40, 0., 40.));
  fOutputContainer->Add(new TH1I("hCellMultClu", "Cell multiplicity per cluster", 200, 0, 200));
  fOutputContainer->Add(new TH1I("hModule", "Module events", 5, 0., 5.));
  fOutputContainer->Add(new TH1F("hCellEnergy", "Cell energy", 1000, 0., 200.));
  fOutputContainer->Add(new TH1I("hCellMultEvent", "PHOS cell multiplicity per event", 2000, 0, 2000));
  fOutputContainer->Add(new TH1I("hClusterMult", "CaloCluster multiplicity", 100, 0, 100));
  fOutputContainer->Add(new TH1F("hClusterEnergy", "Cluster energy", 1000, 0., 200.));
  fOutputContainer->Add(new TH1I("hPHOSClusterMult", "PHOS cluster multiplicity", 100, 0, 100));

  for (Int_t i = 1; i < 5;  ++i)
  {
    fOutputContainer->Add(new TH1I(Form("hCellMultEventM%d", i), Form("PHOS cell multiplicity per event, M%d", i), 2000, 0, 2000));
    fOutputContainer->Add(new TH1I(Form("hPHOSClusterMultM%d", i), Form("PHOS cluster multiplicity, M%d", i), 100, 0, 100));
    fOutputContainer->Add(new TH1F(Form("hCellEnergyM%d", i), Form("Cell energy in module %d", i), 1000, 0., 200.));

    fOutputContainer->Add(new TH1F(Form("hClusterEnergyM%d", i), Form("Cluster energy, M%d", i), 1000, 0., 200.));
    fOutputContainer->Add(new TH2F(Form("hClusterEvsNM%d", i), Form("Cluster energy vs digit multiplicity, M%d", i), 1000, 0., 200., 40, 0., 40.));
    fOutputContainer->Add(new TH2F(Form("hClusterEvsTM%d", i), Form("Cluster energy vs time, M%d", i), 1000, 0., 200., 1200, -6.e-6, +6.e-6));
    fOutputContainer->Add(new TH1I(Form("hCellMultCluM%d", i), Form("Cell multiplicity per cluster, M%d", i), 200, 0, 200));
    fOutputContainer->Add(new TH2F(Form("hCellNXZM%d", i),  Form("Cell  (X,Z), M%d", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
    fOutputContainer->Add(new TH2F(Form("hCellEXZM%d", i),  Form("Cell E(X,Z), M%d", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
    fOutputContainer->Add(new TH2F(Form("hCluNXZM%d_0", i), Form("Clu  (X,Z),  M%d, E>0.5 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
    fOutputContainer->Add(new TH2F(Form("hCluEXZM%d_0", i), Form("Clu E(X,Z),  M%d, E>0.5 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
    fOutputContainer->Add(new TH2F(Form("hCluNXZM%d_1", i), Form("Clu  (X,Z),  M%d, E>1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));
    fOutputContainer->Add(new TH2F(Form("hCluEXZM%d_1", i), Form("Clu E(X,Z),  M%d, E>1 GeV", i), 64, 0.5, 64.5, 56, 0.5, 56.5));

  }



  Int_t    nM    = 750;
  Double_t mMin  = 0.0;
  Double_t mMax  = 1.5;
  Int_t    nPt   = 500;
  Double_t ptMin = 0;
  Double_t ptMax = 100;

  fOutputContainer->Add(new TH2F("hAsymPtPi0", "(A,p_{T})_{#gamma#gamma} #pi^{0}"     , 20, 0., 1.,    40, 0., 20.));
  fOutputContainer->Add(new TH2F("hAsymPtEta", "(A,p_{T})_{#gamma#gamma} #eta"        , 20, 0., 1.,    40, 0., 20.));

  fOutputContainer->Add(new TH2F("hAsymPtPi0M1" , "(A,p_{T})_{#gamma#gamma} #pi^{0}. M1"  , 20, 0., 1.,    40, 0., 20.));
  fOutputContainer->Add(new TH2F("hAsymPtPi0M2" , "(A,p_{T})_{#gamma#gamma} #pi^{0}. M2"  , 20, 0., 1.,    40, 0., 20.));
  fOutputContainer->Add(new TH2F("hAsymPtPi0M3" , "(A,p_{T})_{#gamma#gamma} #pi^{0}. M3"  , 20, 0., 1.,    40, 0., 20.));
  fOutputContainer->Add(new TH2F("hAsymPtPi0M12", "(A,p_{T})_{#gamma#gamma} #pi^{0}. M12" , 20, 0., 1.,    40, 0., 20.));
  fOutputContainer->Add(new TH2F("hAsymPtPi0M23", "(A,p_{T})_{#gamma#gamma} #pi^{0}. M23" , 20, 0., 1.,    40, 0., 20.));

  fOutputContainer->Add(new TH2F("hMassPtA10" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA08" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.8"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA01" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.1"   , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10BC0" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1=BC2=0", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA10BC1" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1!=BC2" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA10BC2" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1=0"    , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10nvtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, no vtx" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07nvtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, no vtx" , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10vtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, vtx"     , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07vtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, vtx"     , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10vtx10", "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, |Zvtx|<10 cm"     , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07vtx10", "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, |Zvtx|<10 cm"     , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10V0AND" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, V0AND", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07V0AND" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, V0AND", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtA10PU" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, pileup", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtA07PU" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, pileup", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtvA10", "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, primary vertex", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtvA07", "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, primary vertex", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH3F("hMassPtCA10", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA10_cpv", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA10_disp", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA10_both", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA07", "(M,p_{T},C)_{#gamma#gamma}, 0<A<0.7" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA07_cpv", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA07_disp", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMassPtCA07_both", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));

  fOutputContainer->Add(new TH2F("hMassSingle_all", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassSingle_cpv", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassSingle_disp", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassSingle_both", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtM1", "(M,p_{T})_{#gamma#gamma}, module 1"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM2", "(M,p_{T})_{#gamma#gamma}, module 2"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM3", "(M,p_{T})_{#gamma#gamma}, module 3"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM4", "(M,p_{T})_{#gamma#gamma}, module 4"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM12", "(M,p_{T})_{#gamma#gamma}, modules 1,2", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM13", "(M,p_{T})_{#gamma#gamma}, modules 1,3", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM23", "(M,p_{T})_{#gamma#gamma}, modules 2,3", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtM34", "(M,p_{T})_{#gamma#gamma}, modules 3,4", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPt20cm", "(M,p_{T})_{#gamma#gamma}, |z|<20 cm"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPt40cm", "(M,p_{T})_{#gamma#gamma}, 20<|z|<40 cm", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPt60cm", "(M,p_{T})_{#gamma#gamma}, |z|>40 cm"   , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5"  , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiAsymPt", "(A,p_{T})_{#gamma#gamma}"                , 50, 0., 1.,    nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA08" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.8"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA01" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.1"   , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10BC0" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1=BC2=0", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA10BC1" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1!=BC2" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA10BC2" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, BC1=0"    , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10nvtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, no vtx" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07nvtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, no vtx" , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10vtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, vtx"     , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07vtx" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, vtx"     , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10vtx10", "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, |Zvtx|<10 cm", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07vtx10", "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, |Zvtx|<10 cm", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10V0AND" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, V0AND", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07V0AND" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, V0AND", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtA10PU" , "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, pileup", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtA07PU" , "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, pileup", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtvA10", "(M,p_{T})_{#gamma#gamma}, 0<A<1.0, primary vertex", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtvA07", "(M,p_{T})_{#gamma#gamma}, 0<A<0.7, primary vertex", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH3F("hMiMassPtCA10", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA10_cpv", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA10_disp", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA10_both", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA07", "(M,p_{T},C)_{#gamma#gamma}, 0<A<0.7" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA07_cpv", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA07_disp", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));
  fOutputContainer->Add(new TH3F("hMiMassPtCA07_both", "(M,p_{T},C)_{#gamma#gamma}, 0<A<1.0" , nM, mMin, mMax, nPt, ptMin, ptMax, 8, 0., 8.));

  fOutputContainer->Add(new TH2F("hMiMassSingle_all", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassSingle_cpv", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassSingle_disp", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassSingle_both", "(M,p_{T})_{#gamma#gamma}, no PID" , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtM1", "(M,p_{T})_{#gamma#gamma}, module 1"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM2", "(M,p_{T})_{#gamma#gamma}, module 2"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM3", "(M,p_{T})_{#gamma#gamma}, module 3"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM4", "(M,p_{T})_{#gamma#gamma}, module 4"    , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM12", "(M,p_{T})_{#gamma#gamma}, modules 1,2", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM13", "(M,p_{T})_{#gamma#gamma}, modules 1,3", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM23", "(M,p_{T})_{#gamma#gamma}, modules 2,3", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtM34", "(M,p_{T})_{#gamma#gamma}, modules 3,4", nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPt20cm", "(M,p_{T})_{#gamma#gamma}, |z|<20 cm"   , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPt40cm", "(M,p_{T})_{#gamma#gamma}, 20<|z|<40 cm", nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPt60cm", "(M,p_{T})_{#gamma#gamma}, |z|>40 cm"   , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH2F("hMiMassPtN3", "(M,p_{T})_{#gamma#gamma}, N_{cell}>2"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtN4", "(M,p_{T})_{#gamma#gamma}, N_{cell}>3"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtN5", "(M,p_{T})_{#gamma#gamma}, N_{cell}>4"  , nM, mMin, mMax, nPt, ptMin, ptMax));
  fOutputContainer->Add(new TH2F("hMiMassPtN6", "(M,p_{T})_{#gamma#gamma}, N_{cell}>5"  , nM, mMin, mMax, nPt, ptMin, ptMax));

  fOutputContainer->Add(new TH1F("hPhotonKappa", "#kappa(#gamma)", 200, 0., 20.));
  fOutputContainer->Add(new TH1F("hPhotonPt", "p_{T}(#gamma)", 200, 0., 20.));
  fOutputContainer->Add(new TH1F("hPhotonPx", "p_{x}(#gamma)", 200, 0., 20.));
  fOutputContainer->Add(new TH1F("hPhotonPy", "p_{y}(#gamma)", 200, 0., 20.));

  fOutputContainer->Add(new TH1F("hNPileupVtx", "Number of SPD pileup vertices", 10, 0., 10.));
  fOutputContainer->Add(new TH1F("hZPileupVtx", "#Delta_{Z} vtx_{0}-vtx_{PU}", 200, -50., +50.));

  fOutputContainer->Add(new TH1F("hZvertex", "Z vertex", 200, -50., +50.));
  fOutputContainer->Add(new TH1F("hNvertexTracks", "N of primary tracks from the primary vertex", 150, 0., 150.));

  fOutputContainer->Add(new TH1F("hV0Atime", "V0A time", 1200, -6.e-6, +6.e-6));
  fOutputContainer->Add(new TH1F("hV0Ctime", "V0C time", 1200, -6.e-6, +6.e-6));
  fOutputContainer->Add(new TH2F("hV0AV0Ctime", "V0A time vs V0C time", 120, -6.e-6, +6.e-6 , 120, -6.e-6, +6.e-6));

  PostData(1, fOutputContainer);

}

//________________________________________________________________________
void AliAnalysisTaskPi0v4::UserExec(Option_t *)
{
  // Main loop, called for each event
  // Analyze AOD

  AliVEvent * event = InputEvent();
  // AliVEvent *event = dynamic_cast<AliVEvent*>(InputEvent());
  if (!event)
  {
    Printf("ERROR: Could not retrieve event");
    return;
  }

  Double_t vtxBest[3];
  EventProperties eprop = SelectEvent(event, vtxBest);

  Int_t centr = 0 ;
  //always zero centrality
  if (!fPHOSEvents[eprop.zvtx][centr]) fPHOSEvents[eprop.zvtx][centr] = new TList() ;
  TList * prevPHOS = fPHOSEvents[eprop.zvtx][centr];

  AliVCaloCells * cells = event->GetPHOSCells();
  FillCellsHistograms(cells);

  Double_t vtx0[3] = {0, 0, 0};
  FillClusterHistograms(event, vtx0);

  // Single loop over clusters fills cluster histograms
  if (fPHOSEvent)
    fPHOSEvent->Clear();
  else
    fPHOSEvent = new TClonesArray("AliCaloPhoton", 50);


  //Select photons for inv mass calculation
  SelectPhotons(event, fPHOSEvent, vtxBest);
  Int_t inPHOS = fPHOSEvent->GetEntriesFast();

  // Fill Real disribution
  for (Int_t i1 = 0; i1 < inPHOS - 1; i1++)
  {
    AliCaloPhoton * ph1 = (AliCaloPhoton *)fPHOSEvent->At(i1) ;
    for (Int_t i2 = i1 + 1; i2 < inPHOS; i2++)
    {
      AliCaloPhoton * ph2 = (AliCaloPhoton *)fPHOSEvent->At(i2) ;
      FillCombinations(ph1, ph2, eprop, "");
    } // end of loop i2
  } // end of loop i1

  //now mixed
  for (Int_t i1 = 0; i1 < inPHOS; i1++)
  {
    AliCaloPhoton * ph1 = (AliCaloPhoton *)fPHOSEvent->At(i1) ;
    for (Int_t ev = 0; ev < prevPHOS->GetSize(); ev++)
    {
      TClonesArray * mixPHOS = static_cast<TClonesArray *>(prevPHOS->At(ev)) ;
      for (Int_t i2 = 0; i2 < mixPHOS->GetEntriesFast(); i2++)
      {
        AliCaloPhoton * ph2 = (AliCaloPhoton *)mixPHOS->At(i2) ;
        FillCombinations(ph1, ph2, eprop, "Mi");
      } // end of loop i2
    }
  } // end of loop i1


  //Now we either add current events to stack or remove
  //If no photons in current event - no need to add it to mixed
  if (fPHOSEvent->GetEntriesFast() > 0)
  {
    prevPHOS->AddFirst(fPHOSEvent) ;
    fPHOSEvent = 0;
    if (prevPHOS->GetSize() > 100) //Remove redundant events
    {
      TClonesArray * tmp = static_cast<TClonesArray *>(prevPHOS->Last()) ;
      prevPHOS->RemoveLast() ;
      delete tmp ;
    }
  }
  // Post output data.
  PostData(1, fOutputContainer);
  fEventCounter++;
}

//________________________________________________________________________
void AliAnalysisTaskPi0v4::Terminate(Option_t *)
{
  // Draw result to the screen
  // Called once at the end of the query

}

//________________________________________________________________________
Bool_t AliAnalysisTaskPi0v4::IsGoodChannel(const char * det, Int_t mod, Int_t ix, Int_t iz)
{
  //Check if this channel belogs to the good ones

  if (strcmp(det, "PHOS") == 0)
  {
    if (mod > 5 || mod < 1)
    {
      AliError(Form("No bad map for PHOS module %d ", mod)) ;
      return kTRUE ;
    }
    if (!fPHOSBadMap[mod])
    {
      AliError(Form("No Bad map for PHOS module %d", mod)) ;
      return kTRUE ;
    }
    if (fPHOSBadMap[mod]->GetBinContent(ix, iz) > 0)
      return kFALSE ;
    else
      return kTRUE ;
  }
  else
    AliError(Form("Can not find bad channels for detector %s ", det)) ;
  return kTRUE ;
}
//_____________________________________________________________________________
void AliAnalysisTaskPi0v4::FillHistogram(const char * key, Double_t x)const
{
  //FillHistogram
  TH1 * hist = dynamic_cast<TH1 *>(fOutputContainer->FindObject(key)) ;
  if (hist)
    hist->Fill(x) ;
  else
    AliError(Form("can not find histogram (of instance TH1) <%s> ", key)) ;
}
//_____________________________________________________________________________
void AliAnalysisTaskPi0v4::FillHistogram(const char * key, Double_t x, Double_t y)const
{
  //FillHistogram
  TH1 * th1 = dynamic_cast<TH1 *> (fOutputContainer->FindObject(key));
  if (th1)
    th1->Fill(x, y) ;
  else
    AliError(Form("can not find histogram (of instance TH1) <%s> ", key)) ;
}

//_____________________________________________________________________________
void AliAnalysisTaskPi0v4::FillHistogram(const char * key, Double_t x, Double_t y, Double_t z) const
{
  //Fills 1D histograms with key
  TObject * obj = fOutputContainer->FindObject(key);

  TH2 * th2 = dynamic_cast<TH2 *> (obj);
  if (th2)
  {
    th2->Fill(x, y, z) ;
    return;
  }
  TH3 * th3 = dynamic_cast<TH3 *> (obj);
  if (th3)
  {
    th3->Fill(x, y, z) ;
    return;
  }

  AliError(Form("can not find histogram (of instance TH2) <%s> ", key)) ;
}

//_____________________________________________________________________________
Bool_t AliAnalysisTaskPi0v4::TestLambda(Double_t l1, Double_t l2)
{
  Double_t l1Mean = 1.22 ;
  Double_t l2Mean = 2.0 ;
  Double_t l1Sigma = 0.42 ;
  Double_t l2Sigma = 0.71 ;
  Double_t c = -0.59 ;
  Double_t R2 = (l1 - l1Mean) * (l1 - l1Mean) / l1Sigma / l1Sigma + (l2 - l2Mean) * (l2 - l2Mean) / l2Sigma / l2Sigma - c * (l1 - l1Mean) * (l2 - l2Mean) / l1Sigma / l2Sigma ;
  return (R2 < 9.) ;
}
//_____________________________________________________________________________
Int_t AliAnalysisTaskPi0v4::TestBC(Double_t tof)
{
  Int_t bc = (Int_t)(TMath::Ceil((tof + fBCgap / 2) / fBCgap) - 1);
  return bc;
}

void AliAnalysisTaskPi0v4::FillCellsHistograms(AliVCaloCells * cells)
{
  Int_t multCells = cells->GetNumberOfCells();
  FillHistogram("hCellMultEvent", multCells);

  // Single loop over cells
  Int_t nCellModule[5] = {0, 0, 0, 0, 0};
  for (Int_t iCell = 0; iCell < multCells; iCell++)
  {

    Int_t relId[4];
    Int_t cellAbsId = cells->GetCellNumber(iCell);

    fPHOSGeo->AbsToRelNumbering(cellAbsId, relId);

    Int_t mod1  = relId[0];
    Int_t cellX = relId[2];
    Int_t cellZ = relId[3] ;
    Float_t  energy = cells->GetAmplitude(iCell);

    if (mod1 < 1 || mod1 > 4) continue;
    FillHistogram("hCellEnergy", energy);

    FillHistogram(Form("hCellEnergyM%d", mod1), cells->GetAmplitude(iCell));
    FillHistogram(Form("hCellNXZM%d", mod1), cellX, cellZ, 1.);
    FillHistogram(Form("hCellEXZM%d", mod1), cellX, cellZ, energy);
    nCellModule[mod1]++;
  }
  for (Int_t i = 1; i < 5; ++i) FillHistogram(Form("hCellMultEventM%d", i), nCellModule[i]);
}

void AliAnalysisTaskPi0v4::FillClusterHistograms(AliVEvent * event, Double_t vtx0[3])
{

  Int_t multClust = event->GetNumberOfCaloClusters();
  FillHistogram("hClusterMult", multClust);

  // Single loop over clusters fills cluster histograms
  Int_t    multPHOSClust[5]  = {0, 0, 0, 0, 0};
  for (Int_t i1 = 0; i1 < multClust; i1++)
  {
    AliVCluster * clu1 = event->GetCaloCluster(i1);
    if ( !clu1->IsPHOS() ) continue;
    if (  clu1->GetType() != AliVCluster::kPHOSNeutral) continue;

    Int_t digMult = clu1->GetNCells();
    Float_t  position[3];
    clu1->GetPosition(position);
    TVector3 global1(position) ;
    Int_t relId[4];

    fPHOSGeo->GlobalPos2RelId(global1, relId) ;
    Int_t mod1  = relId[0];
    Int_t cellX = relId[2];
    Int_t cellZ = relId[3];
    if ( !IsGoodChannel("PHOS", mod1, cellX, cellZ) ) continue ;

    // cellAbsId = clu1->GetCellAbsId(0);
    // fPHOSGeo->AbsToRelNumbering(cellAbsId,relId);
    // mod1   = relId[0];
    Float_t energy = clu1->E();
    Float_t tof    = clu1->GetTOF();

    // Printf("\tmodule=%d, xyz=(%.3f,%.3f,%.3f) cm, E=%.3f GeV",
    //     mod1,position[0],position[1],position[2],energy);

    multPHOSClust[0]++;
    FillHistogram("hClusterEnergy", energy);
    FillHistogram("hClusterEvsN", energy, digMult);
    FillHistogram("hCellMultClu", digMult);
    if (mod1 < 1 || mod1 > 4) continue;

    multPHOSClust[mod1]++;
    FillHistogram(Form("hClusterEvsNM%d", mod1), energy, digMult);
    FillHistogram(Form("hClusterEvsTM%d", mod1), energy, tof);
    FillHistogram(Form("hCellMultCluM%d", mod1), digMult);
    FillHistogram(Form("hClusterEnergyM%d", mod1), energy);
    if (energy > 0.5)
    {
      FillHistogram(Form("hCluNXZM%d_0", mod1), cellX, cellZ, 1.);
      FillHistogram(Form("hCluEXZM%d_0", mod1), cellX, cellZ, energy);
    }
    if (energy > 1.0)
    {
      FillHistogram(Form("hCluNXZM%d_1", mod1), cellX, cellZ, 1.);
      FillHistogram(Form("hCluEXZM%d_1", mod1), cellX, cellZ, energy);
    }

    if (digMult > 2)
    {
      TLorentzVector p1;
      clu1 ->GetMomentum(p1 , vtx0);
      Double_t pAbs = p1.P();
      Double_t pT   = p1.Pt();
      Double_t pX   = p1.Px();
      Double_t pY   = p1.Py();
      if (pAbs < 1.e-10) break;
      Double_t kappa = pAbs - TMath::Power(0.135, 2) / 4. / pAbs;

      FillHistogram("hPhotonKappa", kappa);
      FillHistogram("hPhotonPt", pT);
      FillHistogram("hPhotonPx", pX);
      FillHistogram("hPhotonPy", pY);
    }
  }

  FillHistogram("hPHOSClusterMult"  , multPHOSClust[0]);
  for (Int_t i = 1; i < 5; ++i)
    FillHistogram(Form("hPHOSClusterMultM%d", i), multPHOSClust[i]);
}

void AliAnalysisTaskPi0v4::SelectPhotons(AliVEvent * event, TClonesArray * fPHOSEvent, Double_t vtxBest[3])
{
  Int_t inPHOS = 0 ;
  Int_t multClust = event->GetNumberOfCaloClusters();
  for (Int_t i1 = 0; i1 < multClust; i1++)
  {
    AliVCluster * clu1 = event->GetCaloCluster(i1);
    if ( !clu1->IsPHOS() || clu1->E() < 0.3) continue;
    if (  clu1->GetType() != AliVCluster::kPHOSNeutral) continue;

    Float_t  position[3];
    clu1->GetPosition(position);
    TVector3 global1(position);
    Int_t relId[4];

    fPHOSGeo->GlobalPos2RelId(global1, relId) ;
    Int_t mod1  = relId[0];
    Int_t cellX = relId[2];
    Int_t cellZ = relId[3];
    if ( !IsGoodChannel("PHOS", mod1, cellX, cellZ) ) continue ;

    if (mod1 < 1 || mod1 > 4)
    {
      AliError(Form("Wrong module number %d", mod1));
      return;
    }

    //..................................................
    // Apply module misalignment if analyzing ESD
    if (dynamic_cast<AliESDEvent *> (event))
    {

      Float_t dXmodule[4] = { -2.30, -2.11, -1.53, 0.00}; // X-shift in local system for module 1,2,3,4
      Float_t dZmodule[4] = { -0.40, +0.52, +0.80, 0.00}; // Z-shift in local system for module 1,2,3,4

      TVector3 globalXYZ(position[0], position[1], position[2]);
      TVector3 localXYZ;
      fPHOSGeo->Global2Local(localXYZ, globalXYZ, mod1) ;
      fPHOSGeo->Local2Global(mod1, localXYZ.X() + dXmodule[mod1 - 1], localXYZ.Z() + dZmodule[mod1 - 1], globalXYZ);
      for (Int_t ixyz = 0; ixyz < 3; ixyz++) position[ixyz] = globalXYZ[ixyz] ;
      clu1->SetPosition(position) ;
    }

    //..................................................

    TLorentzVector p1, pv1;
    Double_t vtx0[3] = {0, 0, 0};
    clu1 ->GetMomentum(p1 , vtx0);
    clu1 ->GetMomentum(pv1, vtxBest);

    p1 *= fRecalib[mod1 - 1];

    // Int_t digMult   = clu1->GetNCells();
    new((*fPHOSEvent)[inPHOS]) AliCaloPhoton(p1.X(), p1.Py(), p1.Z(), p1.E()) ;
    AliCaloPhoton * ph = (AliCaloPhoton *)fPHOSEvent->At(inPHOS) ;
    ph->SetModule(mod1) ;
    ph->SetMomV2(&pv1) ;
    ph->SetNCells(clu1->GetNCells());
    ph->SetEMCx(global1.X());
    ph->SetEMCy(global1.Y());
    ph->SetEMCz(global1.Z());
    ph->SetDispBit(TestLambda(clu1->GetM20(), clu1->GetM02())) ;
    ph->SetCPVBit(clu1->GetEmcCpvDistance() > 10.) ;
    ph->SetBC(TestBC(clu1->GetTOF()));

    inPHOS++ ;
  }
}

void AliAnalysisTaskPi0v4::FillCombinations(AliCaloPhoton * ph1, AliCaloPhoton * ph2, const EventProperties & eprop, const char * suff)
{
  TLorentzVector p12  = *ph1  + *ph2;
  TLorentzVector pv12 = *(ph1->GetMomV2()) + *(ph2->GetMomV2());

  Bool_t mainBC = (ph1->GetBC() == 0 && ph2->GetBC() == 0);
  Bool_t mainBC1 = (ph1->GetBC() == 0 || ph2->GetBC() == 0);
  Bool_t diffBC = ((ph1->GetBC() == 0 && ph2->GetBC() != ph1->GetBC()) ||
                   (ph2->GetBC() == 0 && ph2->GetBC() != ph1->GetBC()));
  Double_t asym  = TMath::Abs((ph1->Energy() - ph2->Energy()) / (ph1->Energy() + ph2->Energy()));
  Double_t ma12 = p12.M();
  Double_t pt12 = p12.Pt();
  Int_t centr = 0;

  if (ph1->GetNCells() > 2 && ph2->GetNCells() > 2)
  {
    FillHistogram(Form("h%sMassPtA10", suff), ma12 , pt12 );
    FillHistogram(Form("h%sMassPtvA10", suff), pv12.M(), pv12.Pt());
    FillHistogram(Form("h%sMassPtCA10", suff), ma12 , pt12, centr + 0.5);
    FillHistogram(Form("h%sMassSingle_all", suff), ma12, ph1->Pt()) ;
    FillHistogram(Form("h%sMassSingle_all", suff), ma12, ph2->Pt()) ;
    if (mainBC)
      FillHistogram(Form("h%sMassPtA10BC0", suff), ma12 , pt12 );
    if (diffBC)
      FillHistogram(Form("h%sMassPtA10BC1", suff), ma12 , pt12 );
    if (mainBC1)
      FillHistogram(Form("h%sMassPtA10BC2", suff), ma12 , pt12 );

    if (!eprop.eventVtxExist)
      FillHistogram(Form("h%sMassPtA10nvtx", suff), ma12 , pt12 );
    if (eprop.eventVtxExist)
      FillHistogram(Form("h%sMassPtA10vtx", suff)  , ma12 , pt12 );
    if (eprop.eventVtxExist & eprop.eventVtxZ10cm)
      FillHistogram(Form("h%sMassPtA10vtx10", suff), ma12 , pt12 );
    if (eprop.eventV0AND)
      FillHistogram(Form("h%sMassPtA10V0AND", suff), ma12 , pt12 );
    if (eprop.eventPileup)
      FillHistogram(Form("h%sMassPtA10PU", suff)   , ma12 , pt12 );

    if (ph1->IsCPVOK())
      FillHistogram(Form("h%sMassSingle_cpv", suff), ma12, ph1->Pt()) ;
    if (ph2->IsCPVOK())
      FillHistogram(Form("h%sMassSingle_cpv", suff), ma12, ph2->Pt()) ;
    if (ph1->IsDispOK())
      FillHistogram(Form("h%sMassSingle_disp", suff), ma12, ph1->Pt()) ;
    if (ph2->IsDispOK())
      FillHistogram(Form("h%sMassSingle_disp", suff), ma12, ph2->Pt()) ;
    if (ph1->IsCPVOK() && ph1->IsDispOK())
      FillHistogram(Form("h%sMassSingle_both", suff), ma12, ph1->Pt()) ;
    if (ph2->IsCPVOK() && ph2->IsDispOK())
      FillHistogram(Form("h%sMassSingle_both", suff), ma12, ph2->Pt()) ;


    if (ph1->IsCPVOK() && ph2->IsCPVOK())
      FillHistogram(Form("h%sMassPtCA10_cpv", suff), ma12 , pt12, centr + 0.5);
    if (ph1->IsDispOK() && ph2->IsDispOK())
    {
      FillHistogram(Form("h%sMassPtCA10_disp", suff), ma12 , pt12, centr + 0.5);
      if (ph1->IsCPVOK() && ph2->IsCPVOK())
        FillHistogram(Form("h%sMassPtCA10_both", suff), ma12 , pt12, centr + 0.5);
    }
    if (asym < 0.8)
      FillHistogram(Form("h%sMassPtA08", suff), ma12, pt12);
    if (asym < 0.7)
    {
      FillHistogram(Form("h%sMassPtA07", suff), ma12, pt12);
      FillHistogram(Form("h%sMassPtvA07", suff), pv12.M(), pv12.Pt());
      FillHistogram(Form("h%sMassPtCA07", suff), ma12 , pt12, centr + 0.5);
      if (!eprop.eventVtxExist)
        FillHistogram(Form("h%sMassPtA07nvtx", suff), ma12 , pt12 );
      if (eprop.eventVtxExist)
        FillHistogram(Form("h%sMassPtA07vtx", suff)  , ma12 , pt12 );
      if (eprop.eventVtxExist && eprop.eventV0AND)
        FillHistogram(Form("h%sMassPtA07V0AND", suff), ma12 , pt12 );
      if (eprop.eventPileup)
        FillHistogram(Form("h%sMassPtA07PU", suff)   , ma12 , pt12 );
      if (ph1->IsCPVOK() && ph2->IsCPVOK())
        FillHistogram(Form("h%sMassPtCA07_cpv", suff), ma12 , pt12, centr + 0.5);
      if (ph1->IsDispOK() && ph2->IsDispOK())
      {
        FillHistogram(Form("h%sMassPtCA07_disp", suff), ma12 , pt12, centr + 0.5);
        if (ph1->IsCPVOK() && ph2->IsCPVOK())
          FillHistogram(Form("h%sMassPtCA07_both", suff), ma12 , pt12, centr + 0.5);
      }

    }
    if (asym < 0.1)
      FillHistogram(Form("h%sMassPtA01", suff), ma12, pt12);
    if (TMath::Abs(ma12 - 0.135) < 0.03)
      FillHistogram(Form("h%sAsymPtPi0", suff), asym   , pt12);
    if (TMath::Abs(ma12 - 0.547) < 0.09)
      FillHistogram(Form("h%sAsymPtEta", suff), asym   , pt12);

    if (ph1->Module() == 1 && ph2->Module() == 1)
    {
      FillHistogram(Form("h%sMassPtM1", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M1", suff), asym   , pt12);
    }
    if (ph1->Module() == 2 && ph2->Module() == 2)
    {
      FillHistogram(Form("h%sMassPtM2", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M2", suff), asym   , pt12);
    }
    if (ph1->Module() == 3 && ph2->Module() == 3)
    {
      FillHistogram(Form("h%sMassPtM3", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M3", suff), asym   , pt12);
    }
    if (ph1->Module() == 4 && ph2->Module() == 4)
    {
      FillHistogram(Form("h%sMassPtM4", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M4", suff), asym   , pt12);
    }
    if ((ph1->Module() == 1 && ph2->Module() == 2) ||
        (ph1->Module() == 2 && ph2->Module() == 1))
    {
      FillHistogram(Form("h%sMassPtM12", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M12", suff), asym   , pt12);
    }
    if ((ph1->Module() == 2 && ph2->Module() == 3) ||
        (ph1->Module() == 3 && ph2->Module() == 2))
    {
      FillHistogram(Form("h%sMassPtM23", suff), ma12 , pt12 );
      if (TMath::Abs(ma12 - 0.135) < 0.03) FillHistogram(Form("h%sAsymPtPi0M23", suff), asym   , pt12);
    }
    if ((ph1->Module() == 1 && ph2->Module() == 3) ||
        (ph1->Module() == 3 && ph2->Module() == 1)) FillHistogram(Form("h%sMassPtM13", suff), ma12 , pt12 );
    if ((ph1->Module() == 3 && ph2->Module() == 4) ||
        (ph1->Module() == 4 && ph2->Module() == 3)) FillHistogram(Form("h%sMassPtM34", suff), ma12 , pt12 );

    if ( TMath::Abs(ph1->EMCz()) < 20. || TMath::Abs(ph2->EMCz()) < 20.)
      FillHistogram(Form("h%sMassPt20cm", suff), ma12 , pt12 );
    if ((TMath::Abs(ph1->EMCz()) > 20. && TMath::Abs(ph1->EMCz()) < 40.) ||
        (TMath::Abs(ph2->EMCz()) > 20. && TMath::Abs(ph2->EMCz()) < 40.))
      FillHistogram(Form("h%sMassPt40cm", suff), ma12 , pt12 );
    if ( TMath::Abs(ph1->EMCz()) > 40. || TMath::Abs(ph2->EMCz()) > 40.)
      FillHistogram(Form("h%sMassPt60cm", suff), ma12 , pt12 );

  }

  if (ph1->GetNCells() > 3 && ph2->GetNCells() > 3)
    FillHistogram(Form("h%sMassPtN3", suff), ma12 , pt12 );
  if (ph1->GetNCells() > 4 && ph2->GetNCells() > 4)
    FillHistogram(Form("h%sMassPtN4", suff), ma12 , pt12 );
  if (ph1->GetNCells() > 5 && ph2->GetNCells() > 5)
    FillHistogram(Form("h%sMassPtN5", suff), ma12 , pt12 );
  if (ph1->GetNCells() > 6 && ph2->GetNCells() > 6)
    FillHistogram(Form("h%sMassPtN6", suff), ma12 , pt12 );

}

EventProperties AliAnalysisTaskPi0v4::SelectEvent(AliVEvent * event, Double_t vtxBest[3])
{

  FillHistogram("hSelEvents", 0) ; // All events accepted by PSel

  // Select events from the needed trigger class

  TString trigClasses = event->GetFiredTriggerClasses();
  // if (!trigClasses.Contains(fSelectTrigClass)) {
  //   return;
  // }
  AliInfo(Form("Select event with triggers %s", trigClasses.Data()));

  // Event selection flags

  EventProperties eprop(kFALSE, kFALSE, kFALSE, kFALSE, 0);

  const AliVVertex * primaryVertex = event->GetPrimaryVertex();
  if (primaryVertex)
    eprop.eventVtxExist    = kTRUE;

  vtxBest[0] = primaryVertex->GetX();
  vtxBest[1] = primaryVertex->GetY();
  vtxBest[2] = primaryVertex->GetZ();

  FillHistogram("hNvertexTracks", primaryVertex->GetNContributors());
  FillHistogram("hZvertex"      , primaryVertex->GetZ());

  if (TMath::Abs(primaryVertex->GetZ()) < 10. )
    eprop.eventVtxZ10cm = kTRUE;


  // Check for pileup and fill pileup histograms
  if(dynamic_cast<AliESDEvent *> (event))
  {
    AliESDEvent * eventESD = dynamic_cast<AliESDEvent *> (event);
    eprop.eventPileup = eventESD->IsPileupFromSPD();
    if (eprop.eventPileup)
    {
      Int_t nPileupVertices = eventESD->GetNumberOfPileupVerticesSPD();
      FillHistogram("hNPileupVtx", nPileupVertices);

      for (Int_t puVtx = 0; puVtx < nPileupVertices; puVtx++)
      {
        Double_t dZpileup = primaryVertex->GetZ() - eventESD->GetPileupVertexSPD(puVtx)->GetZ();
        FillHistogram("hZPileupVtx", dZpileup);
      }
    }
  }

  if(dynamic_cast<AliAODEvent *> (event))
  {
    AliAODEvent * eventAOD = dynamic_cast<AliAODEvent *> (event);
    eprop.eventPileup = eventAOD->IsPileupFromSPD();
    if (eprop.eventPileup)
    {
      Int_t nPileupVertices = eventAOD->GetNumberOfPileupVerticesSPD();
      FillHistogram("hNPileupVtx", nPileupVertices);

      for (Int_t puVtx = 0; puVtx < nPileupVertices; puVtx++)
      {
        Double_t dZpileup = primaryVertex->GetZ() - eventAOD->GetPileupVertexSPD(puVtx)->GetZ();
        FillHistogram("hZPileupVtx", dZpileup);
      }
    }
  }
  // eprop.eventV0AND = fTriggerAnalysis->IsOfflineTriggerFired(event, AliTriggerAnalysis::kV0AND);

  // Fill event statistics for different selection criteria
  FillHistogram("hSelEvents", 1) ;
  if (eprop.eventVtxExist)
    FillHistogram("hSelEvents", 2) ;
  if (eprop.eventVtxExist && eprop.eventVtxZ10cm)
    FillHistogram("hSelEvents", 3) ;
  if (eprop.eventVtxExist && eprop.eventVtxZ10cm && eprop.eventV0AND)
    FillHistogram("hSelEvents", 4) ;
  if (eprop.eventVtxExist && eprop.eventVtxZ10cm && eprop.eventV0AND && eprop.eventPileup)
    FillHistogram("hSelEvents", 5) ;
  if (eprop.eventPileup)
    FillHistogram("hSelEvents", 6) ;
  if (eprop.eventV0AND)
    FillHistogram("hSelEvents", 7) ;

  Float_t tV0A = event->GetVZEROData()->GetV0ATime();
  Float_t tV0C = event->GetVZEROData()->GetV0CTime();
  FillHistogram("hV0Atime", tV0A);
  FillHistogram("hV0Atime", tV0C);
  FillHistogram("hV0AV0Ctime", tV0A, tV0C);

  //Vtx class z-bin
  eprop.zvtx = (Int_t)((vtxBest[2] + 10.) / 2.) ;
  if (eprop.zvtx < 0) eprop.zvtx = 0 ;
  if (eprop.zvtx > 9) eprop.zvtx = 9 ;

  if(fEventCounter != 0)
    return eprop;

  // Get PHOS rotation matrices from ESD and set them to the PHOS geometry
  if (dynamic_cast<AliESDEvent *>(event))
  {
    // Initialize the PHOS geometry
    fPHOSGeo = AliPHOSGeometry::GetInstance("Run2") ;
    for (Int_t mod = 0; mod < 5; mod++)
    {
      if (!event->GetPHOSMatrix(mod)) continue;
      fPHOSGeo->SetMisalMatrix(event->GetPHOSMatrix(mod), mod) ;
      Printf("PHOS geo matrix %p for module # %d is set\n", event->GetPHOSMatrix(mod), mod);
    }
  }

  if (dynamic_cast<AliAODEvent *>(event))
  {
    AliOADBContainer geomContainer("phosGeo");
    geomContainer.InitFromFile("$ALICE_PHYSICS/OADB/PHOS/PHOSGeometry.root", "PHOSRotationMatrixes");

    Int_t runNumber = event->GetRunNumber();
    TObjArray * matrixes = (TObjArray *)geomContainer.GetObject(runNumber, "PHOSRotationMatrixes");
    fPHOSGeo =  AliPHOSGeometry::GetInstance("Run2") ;
    for (Int_t mod = 0; mod < 5; mod++)
    {
      if (!matrixes->At(mod))
      {
        if ( fDebug )
          AliInfo(Form("No PHOS Matrix for mod:%d, geo=%p\n", mod, fPHOSGeo));
        continue;
      }
      else
      {
        fPHOSGeo->SetMisalMatrix(((TGeoHMatrix *)matrixes->At(mod)), mod) ;
        if ( fDebug > 1 )
          AliInfo(Form("Adding PHOS Matrix for mod:%d, geo=%p\n", mod, fPHOSGeo));
      }
    }
  }

  return eprop;
}
