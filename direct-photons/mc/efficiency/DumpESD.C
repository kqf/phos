#if !defined(__CINT__) || defined(__MAKECINT__)

#include "TTree.h"
#include "TString.h"
#include "TH3F.h"
#include "TH1S.h"
#include "TArrayS.h"
#include "TFile.h"
#include "TStopwatch.h"
#include "iostream.h"

#include "AliLog.h"
#include "AliESDEvent.h"
#include "AliESDCaloCluster.h"
#include "AliPHOSGeometry.h"

#endif

void DumpESD(Bool_t printCell=kFALSE)
{
  // Macro reads ESD and prints CaloClusters and CaloCells
  // Yuri Kharlov. 25.01.2008

 gSystem->Load ( "libCore.so" );
    gSystem->Load ( "libGeom.so" );
    gSystem->Load ( "libVMC.so" );
    gSystem->Load ( "libPhysics.so" );
    gSystem->Load ( "libTree.so" );
    gSystem->Load ( "libMinuit.so" );
    gSystem->Load ( "libProof.so" );
    //load analysis framework
    //gSystem->Load( "libANALYSIS" );
    //gSystem->Load( "libANALYSISalice" );
    gROOT->ProcessLine(".include $ALICE_ROOT/include");

    //add include path
    gSystem->AddIncludePath( "-I$ALICE_ROOT/include" );
    gSystem->AddIncludePath( "-I$ALICE_ROOT/PHOS" );

    // AliROOT
    gSystem->Load ( "libSTEERBase.so" );
    gSystem->Load ( "libESD.so" );
    gSystem->Load ( "libAOD.so" );
    gSystem->Load ( "libANALYSIS.so" );
    gSystem->Load ( "libANALYSISalice.so" );
    // AliROOT + PHOS
    gSystem->Load("libCDB.so");
    gSystem->Load("libRAWDatabase.so");
    gSystem->Load("libSTEER.so");

    gSystem->Load("libPHOSUtils.so");
    gSystem->Load("libPHOSbase.so");
    gSystem->Load("libPWGGAPHOSTasks.so");
    gSystem->Load("libPHOSrec.so");
    //


//  TGrid::Connect("alien://");
 // const char* file="alien::///alice/cern.ch/user/p/pkurash/ARtest/AliESDs.root";
  const char* file="AliESDs.root";
  TFile f(file);
  TTree *esdTree = (TTree*)f.Get("esdTree");
  if(!esdTree) {
    cerr << "ESD Tree not found!" << endl;
    return;
  }

  TH1F *hClusters=new TH1F("hClusters", "Cluster energy", 100, 0, 10.);
  TH1F *hMassInv=new TH1F("hMassInv","Invariant Mass", 1000,0., 1.);


  AliESDEvent *event = new AliESDEvent;
  event->ReadFromTree(esdTree);



  AliESDCaloCluster *clu1;
  Float_t xyz[3] = {0,0,0};
  Double_t vertex[3] = {0,0,0};


  for(Int_t iEvent=0; iEvent<esdTree->GetEntries(); iEvent++){
    esdTree->GetEvent(iEvent);
    Int_t multClu = event->GetNumberOfCaloClusters();
    AliESDCaloCells *cells = event->GetPHOSCells();
    cout<<endl<<"Event "<<iEvent<<": number of CaloClusters: "
	<<multClu<<", Number of cells "<<cells->GetNumberOfCells()<<endl;

    if (printCell) {
      printf("   All cells in event:\n");
      for (Int_t iCell=0; iCell<cells->GetNumberOfCells(); iCell++) {
	printf("Cell %d, A=%f, n=%d\n",
	       iCell,cells->GetAmplitude(iCell),cells->GetCellNumber(iCell));
      }
    }
    if(!multClu) continue;

     if(multClu==2){  //!!!!!!!!!!!!!!!!!

          clu1 = event->GetCaloCluster(0);
          TLorentzVector p1; clu1->GetMomentum(p1,vertex);

                      
         clu2 = event->GetCaloCluster(1);  
          TLorentzVector p2; clu2->GetMomentum(p2,vertex);

          TLorentzVector p;
          p=p1+p2;

         hMassInv->Fill(p.M());
          
          cout<< "Invariant mass" << p.M()<<endl;


               } //!!!!!!!!!!!!!!!


    for (Int_t i0=0; i0<multClu; i0++) {
      clu1 = event->GetCaloCluster(i0);
      if (clu1->GetType() == 0) continue;
      if (!clu1->IsPHOS()) continue;
      clu1->GetPosition(xyz);
      Float_t   energy     = clu1->E();
      hClusters->Fill(energy); //!!!!!!!!!!!!!!!!!!!!!1
      Int_t     digMult    = clu1->GetNCells();
      printf("Cluster: E=%f, label=%d, xyz=(%.2f,%.2f,%.2f), |EMC-CPV|=%f \n",
	     energy,clu1->GetLabel(),xyz[0],xyz[1],xyz[2],
	     clu1->GetEmcCpvDistance());

      if (printCell) {
	printf("   Cells in cluster %d:\n",i0);
	for (Int_t iDig=0; iDig<digMult; iDig++) {
	  Int_t cellAbsId = clu1->GetCellAbsId(iDig);
	  printf("Digit: absId=%d, cellE=%f\n",
		 cellAbsId, 
		 cells->GetCellAmplitude(cellAbsId)*clu1->GetCellAmplitudeFraction(iDig));
	}
      }
    }
  }

TFile ff("output.root","recreate");
hClusters->Write();
hMassInv->Write();
ff.Close();
}
