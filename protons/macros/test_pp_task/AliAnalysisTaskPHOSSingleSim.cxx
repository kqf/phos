#include "TChain.h"
#include "TTree.h"
#include "TObjArray.h"
#include "TClonesArray.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include "TProfile.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include "TParticle.h"
#include "THnSparse.h"
#include "THashList.h"
#include "TMath.h"

#include "AliAnalysisManager.h"
#include "AliAnalysisTaskSE.h"
#include "AliLog.h"

#include "AliCaloPhoton.h"
#include "AliPHOSGeometry.h"

#include "AliESDtrackCuts.h"
#include "AliESDHeader.h"
#include "AliESDEvent.h"
#include "AliESDCaloCells.h"
#include "AliESDCaloCluster.h"
#include "AliESDVertex.h"
#include "AliESDtrack.h"

#include "AliVEvent.h"
#include "AliVHeader.h"
#include "AliVTrack.h"
#include "AliVCluster.h"
#include "AliVCaloCells.h"

#include "AliMultSelection.h"
#include "AliEventplane.h"
#include "AliQnCorrectionsManager.h"
#include "AliAnalysisTaskFlowVectorCorrections.h"
#include "AliQnCorrectionsQnVector.h"

#include "AliOADBContainer.h"

#include "AliPID.h"
#include "AliPIDResponse.h"

#include "AliAODMCHeader.h"
#include "AliAODHeader.h"
#include "AliAODEvent.h"
#include "AliAODCaloCells.h"
#include "AliAODCaloCluster.h"
#include "AliAODVertex.h"
#include "AliAODTrack.h"
#include "AliAODMCParticle.h"
#include "AliAODInputHandler.h"

#include "AliMCEventHandler.h"
#include "AliMCEvent.h"
#include "AliStack.h"
#include "AliGenEventHeader.h"
#include "AliGenPythiaEventHeader.h"
#include "AliGenCocktailEventHeader.h"

#include "AliAnalysisTaskPHOSSingleSim.h"

// Author: Daiki Sekihata (Hiroshima University)

ClassImp(AliAnalysisTaskPHOSSingleSim)

//________________________________________________________________________
AliAnalysisTaskPHOSSingleSim::AliAnalysisTaskPHOSSingleSim(const char *name):
  AliAnalysisTaskSE(name),
  fOutputContainer(0x0),
  fEvent(0x0),
  fESDEvent(0x0),
  fAODEvent(0x0),
  fMCArrayESD(0x0),
  fMCArrayAOD(0x0),
  fRunNumber(0),
  fPHOSGeo(0x0),
  fPHOSClusterArray(NULL),
  fZvtx(-1)
{
  // Constructor

  for(Int_t i=0;i<10;i++){
      fPHOSEvents[i] = 0;
  }

  for(Int_t i=0;i<3;i++){
    fVertex[i] = 0;
  }



  // Define input and output slots here
  // Input slot #0 works with a TChain
  DefineInput(0, TChain::Class());
  // Output slot #0 id reserved by the base class for AOD
  // Output slot #1 writes into a TH1 container
  DefineOutput(1, THashList::Class());

}
//________________________________________________________________________
AliAnalysisTaskPHOSSingleSim::~AliAnalysisTaskPHOSSingleSim()
{
  for(Int_t i=0;i<10;i++){
    if(fPHOSEvents[i]){
      delete fPHOSEvents[i];
      fPHOSEvents[i] = 0;
    }
  }


}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::UserCreateOutputObjects()
{
  // Create histograms
  // Called once

  fOutputContainer = new THashList();
  fOutputContainer->SetOwner(kTRUE);

  TH1F *hEventSummary = new TH1F("hEventSummary","Event Summary",10,0.5,10.5);
  hEventSummary->GetXaxis()->SetBinLabel(1 ,"all");
  hEventSummary->GetXaxis()->SetBinLabel(2 ,"selected");
  hEventSummary->GetXaxis()->SetBinLabel(3 ,"0PH0 fired");
  hEventSummary->GetXaxis()->SetBinLabel(4 ,"1PHL fired");
  hEventSummary->GetXaxis()->SetBinLabel(5 ,"1PHM fired");
  hEventSummary->GetXaxis()->SetBinLabel(6 ,"1PHH fired");
  hEventSummary->GetXaxis()->SetBinLabel(7 ,"0PH0 fired & matched");
  hEventSummary->GetXaxis()->SetBinLabel(8 ,"1PHL fired & matched");
  hEventSummary->GetXaxis()->SetBinLabel(9 ,"1PHM fired & matched");
  hEventSummary->GetXaxis()->SetBinLabel(10,"1PHH fired & matched");
  fOutputContainer->Add(hEventSummary);


  //event character histogram
  fOutputContainer->Add(new TH1F("hVertexZ","VertexZ",1000,-50.,50.));
  fOutputContainer->Add(new TH1F("hVertexZSelectEvent","VertexZ SelectEvent",1000,-50.,50.));

  fOutputContainer->Add(new TH2F("hVertexXY","VertexXY",100,-0.5,0.5,100,-0.5,0.5));
  fOutputContainer->Add(new TH2F("hVertexXYSelectEvent","VertexXY SelectEvent",100,-0.5,0.5,100,-0.5,0.5));


  //cell QA histograms
  const Int_t Nmod=5;
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCellNXZM%d",imod),Form("Cell N(X,Z) M%d",imod),64,0.5,64.5,56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCellEXZM%d",imod),Form("Cell E(X,Z) M%d",imod),64,0.5,64.5,56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCellAmpTimeM%d_LG",imod),Form("Cell Amplitude vs. Time LG M%d",imod),200,0,20,1000,-500,500));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCellAmpTimeM%d_HG",imod),Form("Cell Amplitude vs. Time HG M%d",imod),200,0,20,1000,-500,500));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH1F(Form("hCellMultEventM%d",imod),Form("PHOS cell multiplicity per event M%d",imod),1001,-0.5,1000.5));

  //cluster QA histograms
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH1F(Form("hPHOSClusterMultM%d",imod)   ,Form("PHOS cluster multiplicity M%d",imod)             ,101,-0.5,100.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH1F(Form("hPHOSClusterMultTOFM%d",imod),Form("PHOS cluster multiplicity M%d with TOF cut",imod),101,-0.5,100.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH1F(Form("hPHOSClusterEnergyM%d",imod)   ,Form("PHOS cluster energy M%d",imod)             ,500,0.,100));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH1F(Form("hPHOSClusterEnergyTOFM%d",imod),Form("PHOS cluster energy M%d with TOF cut",imod),500,0.,100));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluNXZM%d",imod)    ,Form("Cluster N(X,Z) M%d",imod)     ,64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluEXZM%d",imod)    ,Form("Cluster E(X,Z) M%d",imod)     ,64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluLowNXZM%d",imod) ,Form("Cluster Low N(X,Z) M%d",imod) ,64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluLowEXZM%d",imod) ,Form("Cluster Low E(X,Z) M%d",imod) ,64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluHighNXZM%d",imod),Form("Cluster High N(X,Z) M%d",imod),64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluHighEXZM%d",imod),Form("Cluster High E(X,Z) M%d",imod),64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluNXZTOFM%d",imod) ,Form("Cluster N(X,Z) M%d TOF",imod) ,64,0.5,64.5, 56,0.5,56.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCluEXZTOFM%d",imod) ,Form("Cluster E(X,Z) M%d TOF",imod) ,64,0.5,64.5, 56,0.5,56.5));

  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hClusterEvsNM%d",imod),Form("Cluster E vs N_{cell} M%d;E (GeV);N_{cell}",imod),500,0,50,100,0.5,100.5));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hClusterEvsTM%d",imod),Form("Cluster E vs TOF M%d;E (GeV);TOF (ns)",imod)     ,500,0,50, 1000,-500,500));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hClusterEvsM02M%d",imod),Form("Cluster E vs M02 M%d;E (GeV);M02 (cm)",imod),500,0,50,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hClusterNvsM02M%d",imod),Form("Cluster N vs M02 M%d;N_{cell};M02 (cm)",imod),100,0.5,100.5,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hFullDispvsFullEM%d",imod),Form("full dispersion vs full E M%d;E (GeV);dipersion (#sigma)",imod),100,0,50,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCoreDispvsCoreEM%d",imod),Form("core dispersion vs core E M%d;E (GeV);dipersion (#sigma)",imod),100,0,50,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hFullDispvsCoreEM%d",imod),Form("full dispersion vs full E M%d;E (GeV);dipersion (#sigma)",imod),100,0,50,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hCoreDispvsFullEM%d",imod),Form("core dispersion vs core E M%d;E (GeV);dipersion (#sigma)",imod),100,0,50,100,0,10));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH2F(Form("hRvsTrackPtM%d",imod),Form("r vs track pT M%d;p_{T}^{track} (GeV/c);cpv (#sigma)",imod)         ,100,0,50,100,0,10));

  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH3F(Form("hdZvsZvsTrackPt_M%d",imod)        ,"dZ vs. Z;Z (cm);dZ (cm);p_{T}^{track} (GeV/c)"           ,160,-80,80,80,-20,20,40,0,20));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH3F(Form("hdXvsXvsTrackPt_plus_M%d",imod)   ,"dX vs. X positive;X (cm);dX (cm);p_{T}^{track +} (GeV/c)",160,-80,80,80,-20,20,40,0,20));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH3F(Form("hdXvsXvsTrackPt_minus_M%d",imod)  ,"dX vs. X negative;X (cm);dX (cm);p_{T}^{track -} (GeV/c)",160,-80,80,80,-20,20,40,0,20));
  for(Int_t imod=1;imod<Nmod;imod++) fOutputContainer->Add(new TH3F(Form("hdZvsZvsTrackPtElectron_M%d",imod),"dZ vs. Z of e^{#pm};Z (cm);dZ (cm);p_{T}^{track} (GeV/c)",160,-80,80,80,-20,20,40,0,20));//for radial displacement

  for(Int_t imod=1;imod<Nmod;imod++){
    fOutputContainer->Add(new TH2F(Form("hEpRatiovsEnergy_M%d_Electron",imod) ,Form("E/p ratio vs. E_{cluster} M%d;E/p;E_{cluster} (GeV)",imod)    ,100,0,2,100,0,50));
    fOutputContainer->Add(new TH2F(Form("hEpRatiovsEnergy_M%d_Others",imod)   ,Form("E/p ratio vs. E_{cluster} M%d;E/p;E_{cluster} (GeV)",imod)    ,100,0,2,100,0,50));
    fOutputContainer->Add(new TH2F(Form("hEpRatiovsTrackPt_M%d_Electron",imod),Form("E/p ratio vs. E_{cluster} M%d;E/p;p_{T}^{track} (GeV/c)",imod),100,0,2,100,0,50));
    fOutputContainer->Add(new TH2F(Form("hEpRatiovsTrackPt_M%d_Others",imod)  ,Form("E/p ratio vs. E_{cluster} M%d;E/p;p_{T}^{track} (GeV/c)",imod),100,0,2,100,0,50));
  }

  fOutputContainer->Add(new TH2F("hEpRatiovsNsigmaElectronTPC","E/p ratio vs. N_{#sigma}^{e};E/p;n#sigma^{e}",100,0,2,100,-5,5));
  fOutputContainer->Add(new TH2F("hTPCdEdx_Electron","TPC dEdx vs. electron momentum;p^{track} (GeV/c);dE/dx (a.u.)"    ,40,0,20,200,0,200));
  fOutputContainer->Add(new TH2F("hTPCdEdx_Others"  ,"TPC dEdx vs. non-electron momentum;p^{track} (GeV/c);dE/dx (a.u.)",40,0,20,200,0,200));

  fOutputContainer->Add(new TH2F("hClusterEtaPhi","Cluster eta vs. phi;#phi;#eta",63,0,6.3,200,-1,1));
  fOutputContainer->Add(new TH2F("hEnergyvsDistanceToBadChannel","distance to closest bad channel;E (GeV);distance in cell",100,0,50,20,0,10));
  fOutputContainer->Add(new TH2F("hAsymvsMgg","asymmetry vs. M_{#gamma#gamma};asymmetry;M_{#gamma#gamma} (GeV/c^{2})",10,0,1,60,0,0.24));
  fOutputContainer->Add(new TH2F("hAsymvsPt" ,"asymmetry vs. p_{T}^{#gamma#gamma};asymmetry;p_{T} (GeV/c)",10,0,1,100,0,50));

  //<- histograms for QA
  //histograms for physics analysis ->

  const Int_t NpTgg = 101;
  Double_t pTgg[NpTgg]={};

  for(Int_t i=0;i<50;i++)     pTgg[i] = 0.1 * i;            //every 0.1 GeV/c, up to 5 GeV/c
  for(Int_t i=50;i<60;i++)    pTgg[i] = 0.5 * (i-50) + 5.0; //every 0.5 GeV/c, up to 10 GeV/c
  for(Int_t i=60;i<NpTgg;i++) pTgg[i] = 1.0 * (i-60) + 10.0;//every 1.0 GeV/c, up to 50 GeV/c

  const Int_t Nm = 241;
  Double_t mgg[Nm] = {};
  for(Int_t i=0;i<Nm;i++) mgg[i] = 0.004*i;

  const Double_t EventPlane[] = {0,15,30,45,60,75,90,105,120,135,150,165,180};
  const Int_t Nep = sizeof(EventPlane)/sizeof(EventPlane[0]);

  //photon pT histograms
  TH2F *h2PhotonPt = new TH2F("hPhotonPt","Photon Pt;p_{T} (GeV/c);#Delta#phi (deg)",NpTgg-1,pTgg,Nep-1,EventPlane);
  h2PhotonPt->Sumw2();
  fOutputContainer->Add(h2PhotonPt);



  const TString Asym[] = {"","_asym08"};
  const Int_t Nasym = sizeof(Asym)/sizeof(Asym[0]);

  //Mgg vs. pT histogram
  for(Int_t iasym=0;iasym<Nasym;iasym++){
    TH3F *h3 = new TH3F(Form("hMgg%s",Asym[iasym].Data()),"Invariant Mass with 2#gamma;M_{#gamma#gamma} (GeV/c^{2});p_{T} (GeV/c);#Delta#phi (deg.)",Nm-1,mgg,NpTgg-1,pTgg,Nep-1,EventPlane);
    h3->Sumw2();
    fOutputContainer->Add(h3);

    TH3F *h3Mix = new TH3F(Form("hMixMgg%s",Asym[iasym].Data()),"Mix Invariant Mass with 2#gamma;M_{#gamma#gamma} (GeV/c^{2});p_{T} (GeV/c);#Delta#phi (deg.)",Nm-1,mgg,NpTgg-1,pTgg,Nep-1,EventPlane);
    h3Mix->Sumw2();
    fOutputContainer->Add(h3Mix);

  }//end of asymmetry loop

  //<- histograms for physics analysis

  const Int_t NpTggModule = 71;
  Double_t pTggModule[NpTggModule]={};
  for(Int_t i=0;i<50;i++)     pTggModule[i] = 0.1 * i;            //every 0.1 GeV/c, up to 5 GeV/c
  for(Int_t i=50;i<60;i++)    pTggModule[i] = 0.5 * (i-50) + 5.0; //every 0.5 GeV/c, up to 10 GeV/c
  for(Int_t i=60;i<NpTggModule;i++) pTggModule[i] = 1.0 * (i-60) + 10.0;//every 1.0 GeV/c, up to 20 GeV/c

  for(Int_t imod1=1;imod1<Nmod;imod1++){
    for(Int_t imod2=imod1;imod2<Nmod;imod2++){
      if(imod2 - imod1 > 1) continue;

      TH2F *h2 = new TH2F(Form("hMgg_M%d%d",imod1,imod2),"M_{#gamma#gamma} vs p_{T}",60,0,0.24,NpTggModule-1,pTggModule);
      h2->Sumw2();
      fOutputContainer->Add(h2);
    }
  }
  for(Int_t imod1=1;imod1<Nmod;imod1++){
    for(Int_t imod2=imod1;imod2<Nmod;imod2++){
      if(imod2 - imod1 > 1) continue;

      TH2F *h2 = new TH2F(Form("hMixMgg_M%d%d",imod1,imod2),"M_{#gamma#gamma} vs p_{T}",60,0,0.24,NpTggModule-1,pTggModule);
      h2->Sumw2();
      fOutputContainer->Add(h2);
    }
  }




    const TString parname[] = {"Pi0","Eta","Gamma","ChargedPion","ChargedKaon","K0S","K0L","Lambda0","Sigma0"};
    const Int_t Npar = sizeof(parname)/sizeof(parname[0]);

    for(Int_t ipar=0;ipar<Npar;ipar++){
      TH1F *h1Pt = new TH1F(Form("hGen%sPt",parname[ipar].Data()),Form("generated %s pT;p_{T} (GeV/c)",parname[ipar].Data()),NpTgg-1,pTgg);
      h1Pt->Sumw2();
      fOutputContainer->Add(h1Pt);

      TH2F *h2EtaPhi = new TH2F(Form("hGen%sEtaPhi",parname[ipar].Data()),Form("generated %s eta vs phi;#eta;#phi (rad)",parname[ipar].Data()),63,0,6.3,200,-1,1);
      h2EtaPhi->Sumw2();
      fOutputContainer->Add(h2EtaPhi);

      TH2F *h2EtaPt = new TH2F(Form("hGen%sEtaPt",parname[ipar].Data()),Form("generated %s eta vs pT;#eta;p_{T} (GeV/c)",parname[ipar].Data()),200,-1,1,NpTgg-1,pTgg);
      h2EtaPt->Sumw2();
      fOutputContainer->Add(h2EtaPt);

    }//end of particle loop



  PostData(1,fOutputContainer);

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::UserExec(Option_t *option) 
{
  // Main loop
  // Called for each event

  fEvent = dynamic_cast<AliVEvent*>(InputEvent());
  if(!fEvent){
    AliError("event is not available.");
    return;
  }

  fESDEvent = dynamic_cast<AliESDEvent*>(fEvent);
  fAODEvent = dynamic_cast<AliAODEvent*>(fEvent);

  FillHistogramTH1(fOutputContainer,"hEventSummary",1);//all

  const AliVVertex *vVertex = fEvent->GetPrimaryVertex();
  fVertex[0] = vVertex->GetX();
  fVertex[1] = vVertex->GetY();
  fVertex[2] = vVertex->GetZ();
  FillHistogramTH1(fOutputContainer,"hVertexZ" ,fVertex[2]);
  FillHistogramTH2(fOutputContainer,"hVertexXY",fVertex[0],fVertex[1]);
  fZvtx = (Int_t)((fVertex[2]+10.)/2.);//it should be 0-9.
  if(fZvtx < 0) fZvtx = 0;//protection to avoid fZvtx = -1.
  if(fZvtx > 9) fZvtx = 9;//protection to avoid fZvtx = 10.

  //<- end of event selection
  //-> start physics analysis

  FillHistogramTH1(fOutputContainer,"hVertexZSelectEvent" ,fVertex[2]);
  FillHistogramTH2(fOutputContainer,"hVertexXYSelectEvent",fVertex[0],fVertex[1]);
  FillHistogramTH1(fOutputContainer,"hEventSummary",2);//selected event

  if(fRunNumber != fEvent->GetRunNumber()){ // Check run number
    fRunNumber = fEvent->GetRunNumber();
    fPHOSGeo = AliPHOSGeometry::GetInstance();
  }


  ProcessMC();
  if(fPHOSClusterArray) fPHOSClusterArray->Clear();
  else fPHOSClusterArray = new TClonesArray("AliCaloPhoton",100);

  if(!fPHOSEvents[fZvtx]) fPHOSEvents[fZvtx] = new TList();
  TList *prevPHOS = fPHOSEvents[fZvtx];


  //cell QA
  CellQA();
  //cluster QA

  ClusterQA();

  //if(!fPHOSClusterArray){
  //  AliWarning("fPHOSClusterArray object not found!");
  //  return;
  //}
  //SetMCWeight();

  FillPhoton();
  FillMgg();
  FillMixMgg();

  //Now we either add current events to stack or remove
  //If no photons in current event - no need to add it to mixed
  if(fPHOSClusterArray->GetEntriesFast() > 0){
    //don't call fPHOSClucster=0; this will affect original array provided from PHOSbjectCreator.
    //prevPHOS->AddFirst(fPHOSClusterArray);
    //fPHOSClusterArray=0;

    TClonesArray *clone = new TClonesArray(*fPHOSClusterArray);
    prevPHOS->AddFirst(clone);
    //delete clone;
    clone = 0;

    if(prevPHOS->GetSize() > 100){//Remove redundant events
      TClonesArray * tmp = static_cast<TClonesArray*>(prevPHOS->Last());
      prevPHOS->RemoveLast();
      delete tmp;
      tmp = NULL;
    }
  }

  PostData(1, fOutputContainer);
}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::Terminate(Option_t *option) 
{
  //Called once at the end of the query
  //In principle, this function is not needed...

  AliInfo(Form("%s is done.",GetName()));

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::CellQA() 
{
  AliVCaloCells *cells = dynamic_cast<AliVCaloCells*>(fEvent->GetPHOSCells());
  const Int_t multCells = cells->GetNumberOfCells();

  Int_t relId[4]={};
  Int_t nCellModule[5] = {};
  Double_t cellamp=0;
  Double_t celltime=0;
  Int_t module=0,cellx=0,cellz=0;
  Int_t cellAbsId=0;
  Bool_t isHG=kFALSE;

  for(Int_t iCell=0; iCell<multCells; iCell++){
    cellAbsId = cells->GetCellNumber(iCell);

    if(cellAbsId<0) continue;//reject CPV
    isHG = cells->GetCellHighGain(cellAbsId);
    cellamp = cells->GetCellAmplitude(cellAbsId);
    celltime = cells->GetCellTime(cellAbsId);

    fPHOSGeo->AbsToRelNumbering(cellAbsId,relId);

    module = relId[0];
    cellx  = relId[2];
    cellz  = relId[3];

    if(module < 1 || module > 4){
      AliError(Form("Wrong module number %d",module));
      return;
    }

    if(isHG) FillHistogramTH2(fOutputContainer,Form("hCellAmpTimeM%d_HG",module),cellamp,celltime*1e+9);
    else     FillHistogramTH2(fOutputContainer,Form("hCellAmpTimeM%d_LG",module),cellamp,celltime*1e+9);

    nCellModule[module]++;
    FillHistogramTH2(fOutputContainer,Form("hCellNXZM%d",module),cellx,cellz);
    FillHistogramTH2(fOutputContainer,Form("hCellEXZM%d",module),cellx,cellz,cellamp);
  }

  FillHistogramTH1(fOutputContainer,"hCellMultEventM1",nCellModule[1]);
  FillHistogramTH1(fOutputContainer,"hCellMultEventM2",nCellModule[2]);
  FillHistogramTH1(fOutputContainer,"hCellMultEventM3",nCellModule[3]);
  FillHistogramTH1(fOutputContainer,"hCellMultEventM4",nCellModule[4]);

}
//________________________________________________________________________
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::ClusterQA() 
{

  Int_t inPHOS = 0;

  const Int_t multClust = fEvent->GetNumberOfCaloClusters();

  Int_t multPHOSClust[5]={};
  Int_t multPHOSClustTOF[5]={};
  TLorentzVector p1;

  Int_t module=0,cellx=0,cellz=0;
  Int_t relId[4]={};
  Float_t position[3] = {};
  Int_t digMult=0;
  Double_t energy=0,tof=0,eta=0,phi=0;
  Double_t DistToBadChannel = 0;
  Double_t M02=0;
  Double_t R = 0, coreR=0;
  Double_t coreE = 0;
  Double_t r=999, trackPt=0;

  for(Int_t i1=0;i1<multClust;i1++){
    AliVCluster *cluster = (AliVCluster*)fEvent->GetCaloCluster(i1);

    if(cluster->GetType() != AliVCluster::kPHOSNeutral
        || cluster->E() < 0.2 // MIP cut
      ) continue;


    energy  = cluster->E();

    digMult = cluster->GetNCells();
    M02 = cluster->GetM02();

    cluster->GetPosition(position);
    relId[0] = 0; relId[1] = 0; relId[2] = 0; relId[3] = 0;
    TVector3 global1(position);
    fPHOSGeo->GlobalPos2RelId(global1,relId);

    module = relId[0];
    cellx  = relId[2];
    cellz  = relId[3];

    if(module < 1 || module > 4){
      AliError(Form("Wrong module number %d",module));
      return;
    }

    eta = global1.Eta();
    phi = global1.Phi();
    if(phi<0) phi += TMath::TwoPi();
    FillHistogramTH2(fOutputContainer,"hClusterEtaPhi",phi,eta);

    FillHistogramTH2(fOutputContainer,Form("hClusterEvsNM%d",module),energy,digMult);
    FillHistogramTH2(fOutputContainer,Form("hClusterEvsTM%d",module),energy,tof*1e+9);
    FillHistogramTH2(fOutputContainer,Form("hCluNXZM%d",module),cellx,cellz);
    FillHistogramTH2(fOutputContainer,Form("hCluEXZM%d",module),cellx,cellz,energy);

    FillHistogramTH2(fOutputContainer,Form("hClusterEvsM02M%d",module),energy,M02);
    FillHistogramTH2(fOutputContainer,Form("hClusterNvsM02M%d",module),digMult,M02);

    cluster ->GetMomentum(p1,fVertex);
    new((*fPHOSClusterArray)[inPHOS]) AliCaloPhoton(p1.Px(),p1.Py(),p1.Pz(),p1.E());
    AliCaloPhoton * ph = (AliCaloPhoton*)fPHOSClusterArray->At(inPHOS);
    ph->SetModule(module);
    inPHOS++;
  }//end of cluster loop

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillPhoton() 
{
  const Int_t multClust = fPHOSClusterArray->GetEntriesFast();

  Double_t pT=0,energy=0;
  Double_t phi = -999, dphi = -999.;
  Double_t eff=1;
  Double_t value[4] = {};

  Double_t weight = 1.;
  Int_t primary = -1;

  for(Int_t iph=0;iph<multClust;iph++){
    AliCaloPhoton *ph = (AliCaloPhoton*)fPHOSClusterArray->At(iph);
    weight = 1.;


    pT = ph->Pt();
    energy = ph->Energy();
    phi = ph->Phi();



    value[0] = ph->GetNsigmaCPV();
    value[1] = ph->GetNsigmaCoreDisp();
    // value[2] = ph->DistToBadfp();
    value[3] = pT;

    //for PID systematic study


    //0 < photon phi < 2pi
    if(phi < 0) phi += TMath::TwoPi();

    FillHistogramTH2(fOutputContainer,"hPhotonPt",pT,dphi*TMath::RadToDeg(),weight);

    if(ph->IsTOFOK()){
      FillHistogramTH2(fOutputContainer,"hPhotonPt_TOF",pT,dphi*TMath::RadToDeg(),1/eff * weight);
    }

  }//end of cluster loop

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillMgg() 
{
  const Int_t multClust = fPHOSClusterArray->GetEntriesFast();
  TLorentzVector p12, p12core;

  Double_t m12=0,pt12=0,asym=0;
  Double_t e1=0,e2=0;
  Double_t phi = -999, dphi = -999.;

  Double_t eff1=1, eff2=1, eff12=1;

  Double_t weight = 1., w1 = 1., w2 = 1.;

  Int_t primary1 = -1;
  Int_t primary2 = -1;
  Double_t TrueK0SPt = 0;
  Double_t TrueL0Pt = 0;

  Int_t commonID = -1;

  for(Int_t i1=0;i1<multClust-1;i1++){
    AliCaloPhoton *ph1 = (AliCaloPhoton*)fPHOSClusterArray->At(i1);

    for(Int_t i2=i1+1;i2<multClust;i2++){
      AliCaloPhoton *ph2 = (AliCaloPhoton*)fPHOSClusterArray->At(i2);


      e1 = ph1->Energy();
      e2 = ph2->Energy();

      p12  = *ph1 + *ph2;
      m12  = p12.M();
      pt12 = p12.Pt();
      phi  = p12.Phi();
      asym = TMath::Abs((ph1->Energy()-ph2->Energy())/(ph1->Energy()+ph2->Energy()));//always full energy


      eff12 = eff1 * eff2;

      weight = 1.;


      if(TMath::Abs(ph1->Module()-ph2->Module()) < 2) FillHistogramTH2(fOutputContainer,Form("hMgg_M%d%d",TMath::Min(ph1->Module(),ph2->Module()), TMath::Max(ph1->Module(),ph2->Module())),m12,pt12,weight);
      FillHistogramTH3(fOutputContainer,"hMgg",m12,pt12,dphi*TMath::RadToDeg(),weight);

      FillHistogramTH2(fOutputContainer,"hAsymvsMgg",asym,m12,weight);
      if(0.12 < m12 && m12 < 0.15) FillHistogramTH2(fOutputContainer,"hAsymvsPt",asym,pt12,weight);

      if(asym < 0.8) FillHistogramTH3(fOutputContainer,"hMgg_asym08",m12,pt12,dphi*TMath::RadToDeg(),weight);

      if(ph1->IsTOFOK() && ph2->IsTOFOK()){
        FillHistogramTH3(fOutputContainer,"hMgg_TOF",m12,pt12,dphi*TMath::RadToDeg(),1/eff12 * weight);

        if(TMath::Abs(ph1->Module()-ph2->Module()) < 2) FillHistogramTH2(fOutputContainer,Form("hMgg_M%d%d_TOF",TMath::Min(ph1->Module(),ph2->Module()), TMath::Max(ph1->Module(),ph2->Module())),m12,pt12,1/eff12 * weight);

        if(asym < 0.8) FillHistogramTH3(fOutputContainer,"hMgg_TOF_asym08",m12,pt12,dphi*TMath::RadToDeg(),1/eff12 * weight);

      }//end of TOF cut

    }//end of ph2

  }//end of ph1

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillMixMgg() 
{
  TList *prevPHOS = fPHOSEvents[fZvtx];

  const Int_t multClust = fPHOSClusterArray->GetEntriesFast();

  TLorentzVector p12, p12core;
  Double_t m12=0,pt12=0,asym=0;
  Double_t phi = -999, dphi = -999.;
  Double_t weight = 1., w1 = 1., w2 = 1.;

  Double_t eff1=1, eff2=1, eff12=1;
  Double_t e1=0,e2=0;

  for(Int_t i1=0;i1<multClust;i1++){
    AliCaloPhoton *ph1 = (AliCaloPhoton*)fPHOSClusterArray->At(i1);

    for(Int_t ev=0;ev<prevPHOS->GetSize();ev++){
      TClonesArray *mixPHOS = static_cast<TClonesArray*>(prevPHOS->At(ev));

      for(Int_t i2=0;i2<mixPHOS->GetEntriesFast();i2++){
        AliCaloPhoton *ph2 = (AliCaloPhoton*)mixPHOS->At(i2);

        e1 = ph1->Energy();
        e2 = ph2->Energy();

        p12  = *ph1 + *ph2;
        m12  = p12.M();
        pt12 = p12.Pt();
        phi  = p12.Phi();
        asym = TMath::Abs((ph1->Energy()-ph2->Energy())/(ph1->Energy()+ph2->Energy()));

        eff12 = eff1 * eff2;
        weight = 1.;


        FillHistogramTH3(fOutputContainer,"hMixMgg",m12,pt12,dphi*TMath::RadToDeg(),weight);
        if(TMath::Abs(ph1->Module()-ph2->Module()) < 2) FillHistogramTH2(fOutputContainer,Form("hMixMgg_M%d%d",TMath::Min(ph1->Module(),ph2->Module()), TMath::Max(ph1->Module(),ph2->Module())),m12,pt12);

        if(asym < 0.8) FillHistogramTH3(fOutputContainer,"hMixMgg_asym08",m12,pt12,dphi*TMath::RadToDeg(),weight);

        if(ph1->IsTOFOK() && ph2->IsTOFOK()){
          FillHistogramTH3(fOutputContainer,"hMixMgg_TOF",m12,pt12,dphi*TMath::RadToDeg(),1/eff12 * weight);
          if(TMath::Abs(ph1->Module()-ph2->Module()) < 2) FillHistogramTH2(fOutputContainer,Form("hMixMgg_M%d%d_TOF",TMath::Min(ph1->Module(),ph2->Module()), TMath::Max(ph1->Module(),ph2->Module())),m12,pt12,1/eff12);

          if(asym < 0.8) FillHistogramTH3(fOutputContainer,"hMixMgg_TOF_asym08",m12,pt12,dphi*TMath::RadToDeg(),1/eff12 * weight);

        }//end of TOF cut

      }//end of mix

    }//end of ph2

  }//end of ph1

}
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::ProcessMC()
{
  //This is for analyzing general purpose MC such as pure PYTHIA, HIJING, DPMJET, PHOJET and so on.
  //get MC information

  Int_t firstJetindex = -1;
  Int_t lastJetindex  = -1;
  Int_t genIDJet      = -1;
  Int_t firstUEindex  = -1;
  Int_t lastUEindex   = -1;
  Int_t genIDUE       = -1;

  Double_t TruePi0Pt = 1.;
  Double_t TrueK0SPt = 0;

  Int_t genID = -1;
  Double_t pT=0, rapidity=0, phi=0;
  Double_t weight = 1;
  Int_t pdg = 0;
  TString parname = "";
  TString genname = "";
  //Int_t motherid = -1;
  //AliAODMCParticle *mp = 0x0;//mother particle
  //Double_t motherpT = 0;

  if(fESDEvent){//for ESD
    fMCArrayESD = (AliStack*)GetMCInfoESD();
    if(!fMCArrayESD){
      AliError("Could not get MC Stack!");
      return;
    }

    //const Int_t Ntrack = fMCArrayESD->GetNtrack();//this is the number of all particles (event geneartor + GEANT).
    const Int_t Ntrack = fMCArrayESD->GetNprimary();//this is the number of generated particles by event generator.
    for(Int_t i=0;i<Ntrack;i++){
      TParticle *p = (TParticle*)fMCArrayESD->Particle(i);
      Int_t primary = FindPrimaryMotherESD(i);


      pT = p->Pt();
      rapidity = p->Y();
      phi = p->Phi();
      pdg = p->GetPdgCode();

      //rapidity is Y(), but, pseudo-rapidity is Eta();

      if(pT < 1e-3) continue;//reject below 1 MeV
      if(TMath::Abs(rapidity) > 0.5) continue;

      if(p->Rho() > 1.0) continue;
      weight = 1.;

      if(pdg==111){//pi0
        parname = "Pi0";
      }
      else if(pdg==221){//eta
        parname = "Eta";
      }
      else if(pdg==22){//gamma
        parname = "Gamma";
      }
      else if(pdg==211 || pdg==-211){//pi+ or pi-
        //c x tau = 7.8m
        parname = "ChargedPion";
      }
      else if(pdg==321 || pdg==-321){//K+ or K-
        //c x tau = 3.7m
        parname = "ChargedKaon";
      }
      else if(pdg==310){//K0S
        parname = "K0S";
      }
      else if(pdg==130){//K0L
        parname = "K0L";
      }
      else if(pdg==3122){//Lmabda0
        parname = "Lambda0";
      }
      else if(pdg==3212){//Sigma0
        parname = "Sigma0";
      }
      else{
        continue;
      }

      FillHistogramTH1(fOutputContainer,Form("hGen%sPt"    ,parname.Data()),pT          ,weight);
      FillHistogramTH2(fOutputContainer,Form("hGen%sEtaPhi",parname.Data()),phi,rapidity,weight);
      FillHistogramTH2(fOutputContainer,Form("hGen%sEtaPt" ,parname.Data()),rapidity,pT ,weight);

    }//end of generated particle loop

  }//end of ESD
  else if(fAODEvent){//for AOD
    fMCArrayAOD = (TClonesArray*)GetMCInfoAOD();
    if(!fMCArrayAOD){
      AliError("Could not retrieve AOD event!");
      return;
    }

    const Int_t Ntrack = fMCArrayAOD->GetEntriesFast();
    for(Int_t i=0;i<Ntrack;i++){
      AliAODMCParticle *p = (AliAODMCParticle*)fMCArrayAOD->At(i);
      genID = p->GetGeneratorIndex();

      pT = p->Pt();
      rapidity = p->Y();
      phi = p->Phi();
      pdg = p->PdgCode();

      //rapidity is Y(), but, pseudo-rapidity is Eta();

      if(pT < 1e-3) continue;//reject below 1 MeV
      if(TMath::Abs(rapidity) > 0.5) continue;

      if(Rho(p) > 1.0) continue;
      weight = 1.;

      if(pdg==111){//pi0
        parname = "Pi0";
      }
      else if(pdg==221){//eta
        parname = "Eta";
      }
      else if(pdg==22){//gamma
        parname = "Gamma";

      }
      else if(pdg==211 || pdg==-211){//pi+ or pi-
        parname = "ChargedPion";
      }
      else if(pdg==321 || pdg==-321){//K+ or K-
        parname = "ChargedKaon";
      }
      else if(pdg==310){//K0S
        parname = "K0S";
      }
      else if(pdg==130){//K0L
        parname = "K0L";
      }
      else if(pdg==3122){//Lmabda0
        parname = "Lambda0";
      }
      else if(pdg==3212){//Sigma0
        parname = "Sigma0";
      }
      else{
        continue;
      }

      FillHistogramTH1(fOutputContainer,Form("hGen%sPt"    ,parname.Data()),pT          ,weight);
      FillHistogramTH2(fOutputContainer,Form("hGen%sEtaPhi",parname.Data()),phi,rapidity,weight);
      FillHistogramTH2(fOutputContainer,Form("hGen%sEtaPt" ,parname.Data()),rapidity,pT ,weight);

    }//end of generated particle loop


  }


}
//________________________________________________________________________
Double_t AliAnalysisTaskPHOSSingleSim::R(AliAODMCParticle* p)
{
  //Radius of vertex in cylindrical system.

//  if(p->PdgCode() == 111){
//    cout << "Xv = " << p->Xv() << " , fVertex[0] = " << fVertex[0] << endl;
//    cout << "Yv = " << p->Yv() << " , fVertex[1] = " << fVertex[1] << endl;
//    cout << "Zv = " << p->Zv() << " , fVertex[2] = " << fVertex[2] << endl;
//  }

  Double32_t x = p->Xv() - fVertex[0];
  Double32_t y = p->Yv() - fVertex[1];
  return sqrt(x*x + y*y);

  //Double32_t x = p->Xv();
  //Double32_t y = p->Yv();
  //Double32_t z = p->Zv();
  //return sqrt(x*x + y*y + z*z);
}
//________________________________________________________________________
Double_t AliAnalysisTaskPHOSSingleSim::Rho(AliAODMCParticle* p)
{
  //Radius of vertex in spherical system.

//  if(p->PdgCode() == 111){
//    cout << "Xv = " << p->Xv() << " , fVertex[0] = " << fVertex[0] << endl;
//    cout << "Yv = " << p->Yv() << " , fVertex[1] = " << fVertex[1] << endl;
//    cout << "Zv = " << p->Zv() << " , fVertex[2] = " << fVertex[2] << endl;
//  }

  Double32_t x = p->Xv() - fVertex[0];
  Double32_t y = p->Yv() - fVertex[1];
  Double32_t z = p->Zv() - fVertex[2];
  return sqrt(x*x + y*y + z*z);

  //Double32_t x = p->Xv();
  //Double32_t y = p->Yv();
  //Double32_t z = p->Zv();
  //return sqrt(x*x + y*y + z*z);
}
//________________________________________________________________________
//________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillHistogramTH1(TList *list, const Char_t *hname, Double_t x, Double_t w, Option_t *opt) const
{
  //FillHistogram
  TH1 * hist = dynamic_cast<TH1*>(list->FindObject(hname));
  if(!hist){
    AliError(Form("can not find histogram (of instance TH1) <%s> ",hname));
    return;
  }
  else{
    TString optstring(opt);
    Double_t myweight = optstring.Contains("w") ? 1. : w;
    if(optstring.Contains("wx")){
      // use bin width as weight
      Int_t bin = hist->GetXaxis()->FindBin(x);
      // check if not overflow or underflow bin
      if(bin != 0 && bin != hist->GetXaxis()->GetNbins()){
        Double_t binwidth = hist->GetXaxis()->GetBinWidth(bin);
        myweight = w/binwidth;
      }
    }
    hist->Fill(x, myweight);
    return;
  }
}
//_____________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillHistogramTH2(TList *list, const Char_t *name, Double_t x, Double_t y, Double_t w, Option_t *opt) const
{
  TH2 * hist = dynamic_cast<TH2*>(list->FindObject(name));
  if(!hist){
    AliError(Form("can not find histogram (of instance TH2) <%s> ",name));
    return;
  }
  else{
    TString optstring(opt);
    Double_t myweight = optstring.Contains("w") ? 1. : w;
    if(optstring.Contains("wx")){
      Int_t binx = hist->GetXaxis()->FindBin(x);
      if(binx != 0 && binx != hist->GetXaxis()->GetNbins()) myweight *= 1./hist->GetXaxis()->GetBinWidth(binx);
    }
    if(optstring.Contains("wy")){
      Int_t biny = hist->GetYaxis()->FindBin(y);
      if(biny != 0 && biny != hist->GetYaxis()->GetNbins()) myweight *= 1./hist->GetYaxis()->GetBinWidth(biny);
    }
    hist->Fill(x, y, myweight);
    return;
  }
}
//_____________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillHistogramTH3(TList *list, const Char_t *name, Double_t x, Double_t y, Double_t z, Double_t w, Option_t *opt) const
{
  TH3 * hist = dynamic_cast<TH3*>(list->FindObject(name));
  if(!hist){
    AliError(Form("can not find histogram (of instance TH3) <%s> ",name));
    return;
  }
  else{
    TString optstring(opt);
    Double_t myweight = optstring.Contains("w") ? 1. : w;
    if(optstring.Contains("wx")){
      Int_t binx = hist->GetXaxis()->FindBin(x);
      if(binx != 0 && binx != hist->GetXaxis()->GetNbins()) myweight *= 1./hist->GetXaxis()->GetBinWidth(binx);
    }
    if(optstring.Contains("wy")){
      Int_t biny = hist->GetYaxis()->FindBin(y);
      if(biny != 0 && biny != hist->GetYaxis()->GetNbins()) myweight *= 1./hist->GetYaxis()->GetBinWidth(biny);
    }
    if(optstring.Contains("wz")){
      Int_t binz = hist->GetZaxis()->FindBin(z);
      if(binz != 0 && binz != hist->GetZaxis()->GetNbins()) myweight *= 1./hist->GetZaxis()->GetBinWidth(binz);
    }
    hist->Fill(x, y, z, myweight);
    return;
  }
}
//_____________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillProfile(TList *list, const Char_t *name, Double_t x, Double_t y) const
{
  TProfile * hist = dynamic_cast<TProfile*>(list->FindObject(name));
  if(!hist){
    AliError(Form("can not find histogram (of instance TH3) <%s> ",name));
    return;
  }
  else{
    hist->Fill(x,y);
    return;
  }

}
//_____________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::FillSparse(TList *list, const Char_t *name, Double_t *x, Double_t w) const
{
  THnSparse * hist = dynamic_cast<THnSparse*>(list->FindObject(name));
  if(!hist){
    AliError(Form("can not find histogram (of instance THnSparse) <%s> ",name));
    return;
  }
  else{
    hist->Fill(x,w);
    return;
  }

}
//_______________________________________________________________________________
AliStack *AliAnalysisTaskPHOSSingleSim::GetMCInfoESD() 
{
  AliStack *fStack = 0x0;
  AliVEventHandler* eventHandler = AliAnalysisManager::GetAnalysisManager()->GetMCtruthEventHandler();
  if(eventHandler){
    AliMCEventHandler* mcEventHandler = dynamic_cast<AliMCEventHandler*> (eventHandler);
    if(mcEventHandler) fStack = static_cast<AliMCEventHandler*>(AliAnalysisManager::GetAnalysisManager()->GetMCtruthEventHandler())->MCEvent()->Stack();
  }

  if(!fStack) AliError("Could not get MC Stack!");

  return fStack;

}
//_______________________________________________________________________________
TClonesArray *AliAnalysisTaskPHOSSingleSim::GetMCInfoAOD() 
{
  TClonesArray *fMCArray = 0x0;
  AliAODInputHandler* aodHandler=dynamic_cast<AliAODInputHandler*>(AliAnalysisManager::GetAnalysisManager()->GetInputEventHandler());

  if(aodHandler){
    AliAODEvent *aod=aodHandler->GetEvent();
    if(aod){
      fMCArray = dynamic_cast<TClonesArray*>(aod->FindListObject(AliAODMCParticle::StdBranchName()));
      if (!fMCArray) AliError("Could not retrieve MC array!");
    }
    else AliError("Could not retrieve AOD event!");
  }

  return fMCArray;

}
//_______________________________________________________________________________
Int_t AliAnalysisTaskPHOSSingleSim::FindPrimaryMotherESD(Int_t label)
{
  const Int_t Nprimary = fMCArrayESD->GetNprimary();//this number contains only generated particles by event generator.
  //const Int_t Ntrack   = fMCArrayESD->GetNtrack();//this number contains generated particles by event generator + GEANT.
  Int_t tmp = label;
  while(tmp >= Nprimary){
    TParticle *p = (TParticle*)fMCArrayESD->Particle(tmp);
    tmp = p->GetMother(0);//first mother.
  }

  return tmp;
}
//_______________________________________________________________________________
void AliAnalysisTaskPHOSSingleSim::SetMCWeight()
{
  const Int_t multClust = fPHOSClusterArray->GetEntriesFast();

  Double_t weight = 1.;
  Int_t primary = -1;
  Double_t TruePi0Pt = 1.;
  Double_t TrueK0SPt = 0;
  Double_t TrueL0Pt = 0;

  for(Int_t iph=0;iph<multClust;iph++){
    AliCaloPhoton *ph = (AliCaloPhoton*)fPHOSClusterArray->At(iph);
    primary = ph->GetPrimary();
    weight = 1.;

    ph->SetWeight(weight);

  }//end of cluster loop

}
//_______________________________________________________________________________

