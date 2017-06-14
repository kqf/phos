// One can use the configuration macro in compiled mode by
// root [0] gSystem->Load("libgeant321");
// root [0] gSystem->SetIncludePath("-I$ROOTSYS/include -I$ALICE_ROOT/include \
//                   -I$ALICE_ROOT -I$ALICE/geant3/TGeant3");
// root [0] .x grun.C(1,"Config.C++")

/* Config.C file revised by R+Preghenella (preghenella@bo.infn.it)
   
   

 * Still unsolved issues:
 
 - Perugia-2012 tune not supported yet as it needs a different PDF set
 to be linked manually. See PYTHIA log for details. Currently not enabled.
 
 - still using PYTHIA 6.4.25 even though Perugia-2012 tune needs 2.4.28.
 Apparently triggering on particles (Xi and Omega) is not successful with
 PYTHIA 2.4.28
 
 - PHOJET crashes, not yet clear why

*/
   
#if !defined(__CINT__) || defined(__MAKECINT__)
#include <Riostream.h>
#include <TRandom.h>
#include <TDatime.h>
#include <TSystem.h>
#include <TVirtualMC.h>
#include <TGeant3TGeo.h>
#include "STEER/AliRunLoader.h"
#include "STEER/AliRun.h"
#include "STEER/AliConfig.h"
#include "PYTHIA6/AliDecayerPythia.h"
#include "PYTHIA6/AliGenPythia.h"
#include "TDPMjet/AliGenDPMjet.h"
#include "STEER/AliMagFCheb.h"
#include "STRUCT/AliBODY.h"
#include "STRUCT/AliMAG.h"
#include "STRUCT/AliABSOv3.h"
#include "STRUCT/AliDIPOv3.h"
#include "STRUCT/AliHALLv3.h"
#include "STRUCT/AliFRAMEv2.h"
#include "STRUCT/AliFRAMEv3.h"
#include "STRUCT/AliSHILv3.h"
#include "STRUCT/AliPIPEv3.h"
#include "ITS/AliITSv11Hybrid.h"
#include "TPC/AliTPCv2.h"
#include "TOF/AliTOFv6T0.h"
#include "HMPID/AliHMPIDv3.h"
#include "ZDC/AliZDCv3.h"
#include "ZDC/AliZDCv4.h"
#include "TRD/AliTRDv1.h"
#include "TRD/AliTRDgeometry.h"
#include "FMD/AliFMDv1.h"
#include "MUON/AliMUONv1.h"
#include "PHOS/AliPHOSv1.h"
#include "PHOS/AliPHOSSimParam.h"
#include "PMD/AliPMDv1.h"
#include "T0/AliT0v1.h"
#include "EMCAL/AliEMCALv2.h"
#include "ACORDE/AliACORDEv1.h"
#include "VZERO/AliVZEROv7.h"
#include "AD/AliADv1.h"
#endif

enum PDC06Proc_t 
  {
    //
    // PYTHIA-6
    kPythia6,
    kPythia6_Perugia2011,
    kPythia6_Perugia2011_Xi, kPythia6_Perugia2011_Omega,
    kPythia6_Perugia2012,
    kPythia6_Perugia2012_Xi, kPythia6_Perugia2012_Omega,
    //
    // PYTHIA-8
    kPythia8,
    kPythia8_Monash2013,
    kPythia8_Monash2013_Xi, kPythia8_Monash2013_Omega,
    //
    // MORE
    kPhojet,
    kEPOSLHC,
    // PbPb
    kHijing, kBox,
    //
    // single sim
    kPHOSPhoton,
    kPHOSPi0,
    //
    kRunMax
  };

const char * pprRunName[] =
  {
    //
    // PYTHIA-6
    "kPythia6",
    "kPythia6_Perugia2011", 
    "kPythia6_Perugia2011_Xi", "kPythia6_Perugia2011_Omega",
    "kPythia6_Perugia2012",
    "kPythia6_Perugia2012_Xi", "kPythia6_Perugia2012_Omega",
    //
    // PYTHIA-8
    "kPythia8",
    "kPythia8_Monash2013",
    "kPythia8_Monash2013_Xi", "kPythia8_Monash2013_Omega",
    //
    // MORE
    "kPhojet",
    "kEPOSLHC",
    // Pb-Pb
    "kHijing",
    // box test
    "kBox",
    //
    // single sim
    "kPHOSPhoton",
    "kPHOSPi0"
    //
  };

enum Mag_t
  {
    kNoField, k5kG, kFieldMax
  };

const char * pprField[] =
  {
    "kNoField", "k5kG"
  };


enum PprTrigConf_t
  {
    kDefaultPPTrig, kDefaultPbPbTrig
  };

const char * pprTrigConfName[] =
  {
    "p-p","Pb-Pb"
    //    "ocdb","ocdb"
  };

// Geterator, field, beam energy
static PDC06Proc_t   proc     = kPhojet;//Tune350;
static Mag_t         mag      = k5kG;
static Float_t       energy   = -7000; // energy in CMS, if negative, extract from GRP
static Float_t       crossingAngle = 0.; // 0.000280; // beam crossing angle
static Int_t         runNumber = 0;
static PprTrigConf_t strig = kDefaultPbPbTrig; // default pp trigger configuration
//========================//
// Set Random Number seed //
//========================//
TDatime dt;
static UInt_t seed    = dt.Get();

// Comment line
static TString comment;

//--- Functions ---
//
// PYTHIA-6
AliGenerator *MbPythia6(Int_t tune = 0, Int_t ntrig = 0, Int_t *trig = NULL);
//
// PYTHIA-8
AliGenerator *MbPythia8(Int_t tune = 0, Int_t ntrig = 0, Int_t *trig = NULL);
//
// MORE
AliGenerator *MbPhojet();
AliGenerator *MbEPOSLHC();
//

void ProcessEnvironmentVars();
void DetConfig(Int_t year = 2015);
void GenConfig();
void LoadSimLibraries();
void SetupGeant();
void SetupMC();
void SetEnergyFromGRP();

void Config()
{

  // Get settings from environment variables
  ProcessEnvironmentVars();

  LoadSimLibraries();

  gRandom->SetSeed(seed);
  cerr<<"Seed for random number generation= "<<seed<<endl; 

  SetupGeant();
  CreateGAlice();
  DetConfig();
  GenConfig();
  SetupMC();
  printf("\n \n Comment: %s \n \n", comment.Data());  
}

// 
void DetConfig(Int_t year)
{
  //======================//
  //   Define detectors   //
  //======================//

  Int_t iABSO   = 0;
  Int_t iACORDE = 0;
  //Int_t iAD     = year < 2015 ? 0 : 1;
  Int_t iAD     = 0;
  Int_t iDIPO   = 0;
  Int_t iEMCAL  = 0;
  Int_t iFMD    = 0;
  Int_t iFRAME  = 1;
  Int_t iHALL   = 0;
  Int_t iITS    = 1;
  Int_t iMAG    = 1;
  Int_t iMUON   = 0;
  Int_t iPHOS   = 1;
  Int_t iPIPE   = 1;
  Int_t iPMD    = 0;
  Int_t iHMPID  = 0;
  Int_t iSHIL   = 0;
  Int_t iT0     = 0;
  Int_t iTOF    = 1;
  Int_t iTPC    = 1;
  Int_t iTRD    = 1;
  Int_t iVZERO  = 0;
  Int_t iZDC    = 0;
  
  
  //=================== Alice BODY parameters =============================
  AliBODY *BODY = new AliBODY("BODY", "Alice envelop");
  
  
  if (iMAG)
    {
      //=================== MAG parameters ============================
      // --- Start with Magnet since detector layouts may be depending ---
      // --- on the selected Magnet dimensions ---
      AliMAG *MAG = new AliMAG("MAG", "Magnet");
    }
  

  if (iABSO)
    {
      //=================== ABSO parameters ============================
      AliABSO *ABSO = new AliABSOv3("ABSO", "Muon Absorber");
    }

  if (iDIPO)
    {
      //=================== DIPO parameters ============================

      AliDIPO *DIPO = new AliDIPOv3("DIPO", "Dipole version 3");
    }

  if (iHALL)
    {
      //=================== HALL parameters ============================

      AliHALL *HALL = new AliHALLv3("HALL", "Alice Hall");
    }


  if (iFRAME)
    {
      //=================== FRAME parameters ============================

      if (year < 2015) {
 	AliFRAMEv2 *FRAME = new AliFRAMEv2("FRAME", "Space Frame");
	FRAME->SetHoles(1);
      }
      else {
 	AliFRAMEv3 *FRAME = new AliFRAMEv3("FRAME", "Space Frame");
	FRAME->SetHoles(1);
      }
    }

  if (iSHIL)
    {
      //=================== SHIL parameters ============================

      AliSHIL *SHIL = new AliSHILv3("SHIL", "Shielding Version 3");
    }


  if (iPIPE)
    {
      //=================== PIPE parameters ============================

      AliPIPE *PIPE = new AliPIPEv3("PIPE", "Beam Pipe");
    }
 
  if (iITS)
    {
      //=================== ITS parameters ============================

      AliITS *ITS  = new AliITSv11("ITS","ITS v11");
    }

  if (iTPC)
    {
      //============================ TPC parameters =====================

      AliTPC *TPC = new AliTPCv2("TPC", "Default");
    }


  if (iTOF) {
    //=================== TOF parameters ============================

    AliTOF *TOF = new AliTOFv6T0("TOF", "normal TOF");
  }


  if (iHMPID)
    {
      //=================== HMPID parameters ===========================

      AliHMPID *HMPID = new AliHMPIDv3("HMPID", "normal HMPID");
    }


  if (iZDC)
    {
      //=================== ZDC parameters ============================

      if (year < 2015) {
	AliZDC *ZDC = new AliZDCv3("ZDC", "normal ZDC");
	//Collimators aperture
	ZDC->SetVCollSideCAperture(0.85);
	ZDC->SetVCollSideCCentre(0.);
	ZDC->SetVCollSideAAperture(0.75);
	ZDC->SetVCollSideACentre(0.);
	//Detector position
	ZDC->SetYZNC(1.6);
	ZDC->SetYZNA(1.6);
	ZDC->SetYZPC(1.6);
	ZDC->SetYZPA(1.6);
      }
      else {
	AliZDC *ZDC = new AliZDCv4("ZDC", "normal ZDC");
	ZDC->SetLumiLength(0.);
	ZDC->SetVCollSideCAperture(2.8);
	ZDC->SetVCollSideCApertureNeg(2.8);
      }
    }

  if (iTRD)
    {
      //=================== TRD parameters ============================

      AliTRD *TRD = new AliTRDv1("TRD", "TRD slow simulator");
      AliTRDgeometry *geoTRD = TRD->GetGeometry();
      // Partial geometry: modules at 0,1,7,8,9,16,17
      // starting at 3h in positive direction
      if (year < 2015) { // need to be propely set for alla years 
	geoTRD->SetSMstatus(2,0);
	geoTRD->SetSMstatus(3,0);
	geoTRD->SetSMstatus(4,0);
	geoTRD->SetSMstatus(5,0);
	geoTRD->SetSMstatus(6,0);
	geoTRD->SetSMstatus(11,0);
	geoTRD->SetSMstatus(12,0);
	geoTRD->SetSMstatus(13,0);
	geoTRD->SetSMstatus(14,0);
	geoTRD->SetSMstatus(15,0);
	geoTRD->SetSMstatus(16,0);
      }
    }

  if (iFMD)
    {
      //=================== FMD parameters ============================

      AliFMD *FMD = new AliFMDv1("FMD", "normal FMD");
    }

  if (iMUON)
    {
      //=================== MUON parameters ===========================
      // New MUONv1 version (geometry defined via builders)
      AliMUON *MUON = new AliMUONv1("MUON", "default");
      // activate trigger efficiency by cells
      if (year < 2015) {
	MUON->SetTriggerEffCells(1);
      }
      else {
	MUON->SetTriggerResponseV1(2);
      }
    }

  if (iPHOS)
    {
      //=================== PHOS parameters ===========================

      if (year < 2015) {
	AliPHOS *PHOS = new AliPHOSv1("PHOS", "noCPV_Modules123");
      }
      else {
	AliPHOS *PHOS = new AliPHOSv1("PHOS", "Run2");
      }
	
    }


  if (iPMD)
    {
      //=================== PMD parameters ============================

      AliPMD *PMD = new AliPMDv1("PMD", "normal PMD");
    }

  if (iT0)
    {
      //=================== T0 parameters ============================
      AliT0 *T0 = new AliT0v1("T0", "T0 Detector");
    }

  if (iEMCAL)
    {
      //=================== EMCAL parameters ============================

      if (year < 2015) {
	AliEMCAL *EMCAL = new AliEMCALv2("EMCAL", "EMCAL_FIRSTYEARV1");
      }
      else {
	AliEMCAL *EMCAL = new AliEMCALv2("EMCAL", "EMCAL_COMPLETE12SMV1_DCAL_8SM", kFALSE);
      }
	
    }

  if (iACORDE)
    {
      //=================== ACORDE parameters ============================

      AliACORDE *ACORDE = new AliACORDEv1("ACORDE", "normal ACORDE");
    }

  if (iVZERO)
    {
      //=================== ACORDE parameters ============================
      
      AliVZERO *VZERO = new AliVZEROv7("VZERO", "normal VZERO");
    }  

  if (iAD){
    //=================== AD parameters ============================
    AliAD *AD = new AliADv1("AD", "normal AD");
  }         
  
}

void CreateGAlice() 
{
  //=======================================================================
  //  Create the output file
   
  AliRunLoader* rl=0x0;

  cout<<"Config.C: Creating Run Loader ..."<<endl;
  rl = AliRunLoader::Open("galice.root",
			  AliConfig::GetDefaultEventFolderName(),
			  "recreate");
  if (!rl) {
    gAlice->Fatal("Config.C","Can not instatiate the Run Loader");
    return;
  }
  rl->SetCompressionLevel(2);
  rl->SetNumberOfEventsPerFile(1000);
  gAlice->SetRunLoader(rl);
  // gAlice->SetGeometryFromFile("geometry.root");
  // gAlice->SetGeometryFromCDB();
  rl->CdGAFile();
}


void SetupMC()
{
  //======================//
  //    Set MC options    //
  //======================//

  // Set the trigger configuration: proton-proton
  AliSimulation::Instance()->SetTriggerConfig(pprTrigConfName[strig]);
  cout <<"Trigger configuration is set to  "<<pprTrigConfName[strig]<<endl;
  //
  gMC->SetProcess("DCAY",1);
  gMC->SetProcess("PAIR",1);
  gMC->SetProcess("COMP",1);
  gMC->SetProcess("PHOT",1);
  gMC->SetProcess("PFIS",0);
  gMC->SetProcess("DRAY",0);
  gMC->SetProcess("ANNI",1);
  gMC->SetProcess("BREM",1);
  gMC->SetProcess("MUNU",1);
  gMC->SetProcess("CKOV",1);
  gMC->SetProcess("HADR",1);
  gMC->SetProcess("LOSS",2);
  gMC->SetProcess("MULS",1);
  gMC->SetProcess("RAYL",1);
  
  Float_t cut = 1.e-3;        // 1MeV cut by default
  Float_t tofmax = 1.e10;
  
  gMC->SetCut("CUTGAM", cut);
  gMC->SetCut("CUTELE", cut);
  gMC->SetCut("CUTNEU", cut);
  gMC->SetCut("CUTHAD", cut);
  gMC->SetCut("CUTMUO", cut);
  gMC->SetCut("BCUTE",  cut); 
  gMC->SetCut("BCUTM",  cut); 
  gMC->SetCut("DCUTE",  cut); 
  gMC->SetCut("DCUTM",  cut); 
  gMC->SetCut("PPCUTM", cut);
  gMC->SetCut("TOFMAX", tofmax); 
  //
  //======================//
  // Set External decayer //
  //======================//
  TVirtualMCDecayer* decayer = new AliDecayerPythia();
  decayer->SetForceDecay(kAll);
  decayer->Init();
  gMC->SetExternalDecayer(decayer);
  //
}

void VertexSigma(int run, double &sx, double &sy, double &sz)
{
  
  // defualts
  sx = 65E-4; 
  sy = 65E-4;
  sz = 6.0;  // usually set from the mean vertex CDB object
  //
  // tuned on LHC10 pass4 MeanVertex objects, with 10% downscaling
  if (run>=114786&&run<=115193) {sx =  66.E-4; sy =  85.E-4;} // b1005-1019, 9 runs
  else if (run>=115310&&run<=115345) {sx =  72.E-4; sy =  76.E-4;} // b1022-1022, 8 runs
  else if (run>=115393&&run<=115521) {sx =  73.E-4; sy =  72.E-4;} // b1023-1023, 5 runs
  else if (run>=115880&&run<=116081) {sx =  66.E-4; sy =  70.E-4;} // b1031-1031, 7 runs
  else if (run>=116102&&run<=116134) {sx =  80.E-4; sy =  64.E-4;} // b1034-1034, 6 runs
  else if (run>=116198&&run<=116288) {sx =  67.E-4; sy =  73.E-4;} // b1035-1035, 2 runs
  else if (run>=116401&&run<=116403) {sx =  65.E-4; sy =  61.E-4;} // b1044-1044, 3 runs
  else if (run>=116562&&run<=116684) {sx =  67.E-4; sy =  82.E-4;} // b1045-1045, 4 runs
  else if (run>=117034&&run<=118506) {sx =  53.E-4; sy =  56.E-4;} // b1058-1058, 20 runs
  else if (run>=117220&&run<=117222) {sx =  46.E-4; sy =  47.E-4;} // b1059-1059, 2 runs
  else if (run>=118503&&run<=118561) {sx = 213.E-4; sy = 240.E-4;} // b1068-1068, 6 runs
  else if (run>=119037&&run<=119086) {sx =  69.E-4; sy =  66.E-4;} // b1089-1089, 12 runs
  else if (run>=119156&&run<=120244) {sx =  56.E-4; sy =  54.E-4;} // b1090-1090, 4 runs
  else if (run>=120503&&run<=120505) {sx =  59.E-4; sy =  69.E-4;} // b1117-1117, 3 runs
  else if (run>=120611&&run<=120617) {sx =  55.E-4; sy =  61.E-4;} // b1118-1118, 5 runs
  else if (run>=120671&&run<=120822) {sx =  54.E-4; sy =  51.E-4;} // b1119-1119, 2 runs
  else if (run>=120823&&run<=120829) {sx =  52.E-4; sy =  80.E-4;} // b1122-1122, 8 runs
  else if (run>=121039&&run<=121040) {sx = 197.E-4; sy = 232.E-4;} // b1128-1128, 2 runs
  else if (run>=122372&&run<=122375) {sx =  54.E-4; sy =  49.E-4;} // b1134-1134, 3 runs
  else if (run>=124187&&run<=124191) {sx =  60.E-4; sy =  71.E-4;} // b1179-1179, 2 runs
  else if (run>=124355&&run<=124376) {sx =  64.E-4; sy =  55.E-4;} // b1182-1182, 15 runs
  else if (run>=124377&&run<=125296) {sx =  69.E-4; sy =  63.E-4;} // b1182-1182, 15 runs
  else if (run>=125628&&run<=125634) {sx =  74.E-4; sy =  58.E-4;} // b1207-1207, 5 runs
  else if (run>=125842&&run<=125855) {sx =  72.E-4; sy =  67.E-4;} // b1222-1222, 9 runs
  else if (run>=126004&&run<=126097) {sx =  67.E-4; sy =  65.E-4;} // b1224-1224, 3 runs
  else if (run>=126158&&run<=126177) {sx =  70.E-4; sy =  61.E-4;} // b1226-1226, 5 runs
  else if (run>=126158&&run<=126177) {sx =  64.E-4; sy =  62.E-4;} // b1229-1229, 3 runs
  else if (run>=126283&&run<=126285) {sx =  69.E-4; sy =  67.E-4;} // b1232-1232, 4 runs
  else if (run>=126350&&run<=126359) {sx =  63.E-4; sy =  59.E-4;} // b1233-1233, 12 runs
  else if (run>=126403&&run<=126437) {sx =  69.E-4; sy =  65.E-4;} // b1250-1250, 7 runs
  else if (run>=127712&&run<=128192) {sx =  67.E-4; sy =  61.E-4;} // b1251-1251, 6 runs
  else if (run>=127712&&run<=136136) {sx =  68.E-4; sy =  62.E-4;} // b1260-1260, 1 runs
  else {
    ::Info("VertexSigma","no matching run found, defaults will be used");
  }
  ::Info("VertexSigma",Form("Luminous Region set in Config: sX: %.4f sY: %.4f sZ: %.4f",sx,sy,sz));
}

void LoadSimLibraries()
{
  // Libraries
#if defined(__CINT__)
  gSystem->Load("liblhapdf");      // Parton density functions
  gSystem->Load("libEGPythia6");   // TGenerator interface
  gSystem->Load("libgeant321");
  if (proc == kPythia6)// || proc == kPhojet)
    gSystem->Load("libpythia6"); // Pythia 6.2
  else
    gSystem->Load("libpythia6_4_25");   // Pythia 6.4
  //    gSystem->Load("libpythia6_4_28");   // Pythia 6.4
  gSystem->Load("libAliPythia6");  // ALICE specific implementations
#endif
  //
}

//
void GenConfig()
{
  //=========================//
  // Generator Configuration //
  //=========================//
  AliGenerator* gener = 0x0;

  printf("proc = %d\n", proc);

  switch (proc) {
    //
    // PYTHIA-6
    //
  case kPythia6:
    gener = MbPythia6();
    break;
  case kPythia6_Perugia2011:
    gener = MbPythia6(350);
    break;
  case kPythia6_Perugia2011_Xi:
    Int_t trig[2] = {3312, -3312}; 
    gener = MbPythia6(350, 2, trig);
    break;
  case kPythia6_Perugia2011_Omega:
    Int_t trig[2] = {3334, -3334}; 
    gener = MbPythia6(350, 2, trig);
    break;
  case kPythia6_Perugia2012:
    printf("PYTHIA6 Perugia-2012 not supported yet\n");
    exit(1);
    gener = MbPythia6(370);
    break;
  case kPythia6_Perugia2012_Xi:
    printf("PYTHIA6 Perugia-2012 not supported yet\n");
    exit(1);
    Int_t trig[2] = {3312, -3312}; 
    gener = MbPythia6(370, 2, trig);
    break;
  case kPythia6_Perugia2012_Omega:
    printf("PYTHIA6 Perugia-2012 not supported yet\n");
    exit(1);
    Int_t trig[2] = {3334, -3334}; 
    gener = MbPythia6(370, 2, trig);
    break;
    //
    // PYTHIA-8
    //
  case kPythia8:
    gener = MbPythia8();
    break;
  case kPythia8_Monash2013:
    gener = MbPythia8(14);
    break;
  case kPythia8_Monash2013_Xi:
    Int_t trig[2] = {3312, -3312}; 
    gener = MbPythia8(14, 2, trig);
    break;
  case kPythia8_Monash2013_Omega:
    Int_t trig[2] = {3334, -3334}; 
    gener = MbPythia8(14, 2, trig);
    break;
    //
    // MORE
    //
  case kPhojet:
    gener = MbPhojet();
    break;
  case kEPOSLHC:
    gener = MbEPOSLHC();
    break;
  case kHijing:
    gener = Hijing();
    break;
  case kBox:
    gener = Box();
    break;
  case kPHOSPhoton:
    gener = PHOSPhoton();
  case kPHOSPi0:
    gener = PHOSPi0();
    break;
  }
  //    
  //
  double sigmaX,sigmaY,sigmaZ;
  VertexSigma(runNumber, sigmaX, sigmaY, sigmaZ);
  gener->SetOrigin(0.075, 0.522, -0.884); // R+HACK
  gener->SetSigma(65e-4, 65e-4, 5.); // R+HACK
  //  gener->SetSigma(sigmaX, sigmaY, sigmaZ);      // Sigma in (X,Y,Z) (cm) on IP position
  gener->SetVertexSmear(kPerEvent);
  gener->Init();
  //
}

void SetupGeant() 
{
  //=========================//
  // Geant instance, setup   //
  //=========================//
  
  new TGeant3TGeo("C++ Interface to Geant3");
}

//           PYTHIA
//

AliGenerator *MbPythia6(Int_t tune, Int_t ntrig, Int_t *trig)
{
  comment = comment.Append(" pp: Pythia6 low-pt");
  //
  // Pythia
  AliGenPythia* pythia = new AliGenPythia(-1); 
  pythia->SetMomentumRange(0, 999999.);
  pythia->SetThetaRange(0., 180.);
  pythia->SetYRange(-12.,12.);
  pythia->SetPtRange(0,1000.);
  pythia->SetProcess(kPyMb);
  pythia->SetEnergyCMS(energy);
  pythia->SetCrossingAngle(0,crossingAngle);
  //
  // Tune
  if (tune > 0) {
    comment = comment.Append(Form(" | tune %d", tune));
    pythia->SetTune(tune); 
    pythia->UseNewMultipleInteractionsScenario();
  }
  //
  // Trigger particles
  if (ntrig > 0) {
    Int_t pdg = trig[gRandom->Integer(ntrig)];
    comment = comment.Append(Form(" | %s enhanced",
				  TDatabasePDG::Instance()->GetParticle(pdg)->GetName()));
    pythia->SetTriggerParticle(pdg, 1.2);
  }
  //
  return pythia;
}

AliGenerator *MbPythia8(Int_t tune, Int_t ntrig, Int_t *trig)
{
  //
  // Libraries
#if defined(__CINT__)
  gSystem->Load("libpythia8.so");
  gSystem->Load("libAliPythia8.so");
#endif
  //
  //
  comment = comment.Append(" pp: Pythia8 low-pt");
  //
  // Pythia
  AliGenPythiaPlus *pythia = new AliGenPythiaPlus(AliPythia8::Instance()); 
  pythia->SetMomentumRange(0, 999999.);
  pythia->SetThetaRange(0., 180.);
  pythia->SetYRange(-12.,12.);
  pythia->SetPtRange(0,1000.);
  pythia->SetProcess(kPyMbDefault); // pythia->SetProcess(kPyMb);
  pythia->SetEnergyCMS(energy);
  pythia->SetCrossingAngle(0,crossingAngle);
  //
  // Initialize
  pythia->SetEventListRange(-1, 2); 
  (AliPythia8::Instance())->ReadString("Random:setSeed = on");
  (AliPythia8::Instance())->ReadString(Form("Random:seed = %ld", seed%900000000)); 
  //
  // Tune
  if (tune > 0) {
    comment = comment.Append(Form(" | tune %d", tune));
    (AliPythia8::Instance())->ReadString(Form("Tune:pp = %d", tune));
  }
  //
  // Trigger particles
  if (ntrig > 0) {
    Int_t pdg = trig[gRandom->Integer(ntrig)];
    comment = comment.Append(Form(" | %s enhanced",
				  TDatabasePDG::Instance()->GetParticle(pdg)->GetName()));
    pythia->SetTriggerParticle(pdg, 1.2);
  }
  //
  return pythia;
}

AliGenerator* MbPhojet()
{
  comment = comment.Append(" pp: Phojet low-pt");
  //
  //    DPMJET
#if defined(__CINT__)
  gSystem->Load("libDPMJET");
  gSystem->Load("libTDPMjet");
#endif
  AliGenDPMjet* dpmjet = new AliGenDPMjet(-1);
  dpmjet->SetMomentumRange(0, 999999.);
  dpmjet->SetThetaRange(0., 180.);
  dpmjet->SetYRange(-12.,12.);
  dpmjet->SetPtRange(0,1000.);
  dpmjet->SetProcess(kDpmMb);
  dpmjet->SetEnergyCMS(energy);
  dpmjet->SetCrossingAngle(0,crossingAngle);
  return dpmjet;
}

AliGenerator* MbEPOSLHC()
{
  comment = comment.Append(" pp: EPOS-LHC");
  //
  //    EPOS LHC
  printf("--- LAUNCHING CRMC ---\n");
  TString cmd = Form("$CRMC_BASEDIR/bin/crmc -t -c crmc.local.param -f crmceventfifo -o hepmc -p%d -P-%d -n5 -m0", (Int_t)energy / 2, (Int_t)energy / 2);
  printf("%s\n", cmd.Data());
  printf("----- CRMC PARAM -----\n");
  gROOT->ProcessLine(".! cp crmc.param crmc.local.param");
  gROOT->ProcessLine(".! sed -ibak 's,BASEDIR,'\"$CRMC_BASEDIR\"',' crmc.local.param");
  gROOT->ProcessLine(".! cat crmc.local.param");
  printf("----------------------\n");
  gROOT->ProcessLine(".! mkfifo crmceventfifo");
  gROOT->ProcessLine(Form(".! %s &", cmd.Data()));
  
  AliGenReaderHepMC *reader = new AliGenReaderHepMC();
  reader->SetFileName("crmceventfifo");
  AliGenExtFile *gener = new AliGenExtFile(-1);
  gener->SetReader(reader);

  return gener;
}

AliGenerator* Box()
{
  AliGenBox*  gener = new AliGenBox(200);
  gener->SetMomentumRange(1.0, 1.1);
  gener->SetPhiRange(0., 360.);
  gener->SetThetaRange(45., 135.);
  gener->SetOrigin(0, 0, 0);
  gener->SetPart(211);
  gener->SetProjectile("A", 208, 82);
  gener->SetTarget    ("A", 208, 82);

  return gener;
}

AliGenerator* Hijing()
{
  comment = comment.Append(" PbPb: HIJING");
#if defined(__CINT__)
  gSystem->Load("libhijing");
  gSystem->Load("libTHijing");
#endif
  AliGenHijing *gener = new AliGenHijing(-1);
  // centre of mass energy
  gener->SetEnergyCMS(energy);
  gener->SetImpactParameterRange(0., 20.);
  // reference frame
  gener->SetReferenceFrame("CMS");
  // projectile
  gener->SetProjectile("A", 208, 82);
  gener->SetTarget    ("A", 208, 82);
  // tell hijing to keep the full parent child chain
  gener->KeepFullEvent();
  // enable jet quenching
  gener->SetJetQuenching(0);
  // enable shadowing
  gener->SetShadowing(1);
  // neutral pion and heavy particle decays switched off
  gener->SetDecaysOff(1);
  // Don't track spectators
  gener->SetSpectators(0);
  // kinematic selection
  gener->SetSelectAll(0);
  gener->SetPtHardMin(2.3);

}

AliGenerator* PHOSPhoton()
{
  comment = comment.Append(" single simulation : PHOS photon");

  AliGenCocktail *cocktail = new AliGenCocktail();
  cocktail->SetProjectile("A", 208, 82);
  cocktail->SetTarget    ("A", 208, 82);
  cocktail->SetEnergyCMS(energy);
//  comment = comment.Append(" + HIJING");
//      cocktail->AddGenerator(hijing,"hijing",1);

  AliGenBox *gPHSPhoton = new AliGenBox(1);
  gPHSPhoton->SetPart(22);//photon
  gPHSPhoton->SetPtRange(0.,80);
  gPHSPhoton->SetPhiRange(240.,330.);
  gPHSPhoton->SetYRange(-0.13,0.13);
  cocktail->AddGenerator(gPHSPhoton,"gPHSPhoton",1);//for PHOS

  //return gener;
  return cocktail;
}

AliGenerator* PHOSPi0()
{
  comment = comment.Append(" single simulation : PHOS pi0");

  AliGenCocktail *cocktail = new AliGenCocktail();
  //cocktail->SetProjectile("A", 208, 82);
  //cocktail->SetTarget    ("A", 208, 82);
  //cocktail->SetEnergyCMS(energy);
//  comment = comment.Append(" + HIJING");
//  cocktail->AddGenerator(hijing,"hijing",1);

  AliGenBox *gPHSPi0 = new AliGenBox(1);
  gPHSPi0->SetPart(111);//pi0
  gPHSPi0->SetPtRange(0.,45);
  gPHSPi0->SetPhiRange(240.,330.);
  gPHSPi0->SetYRange(-0.15,0.15);
  cocktail->AddGenerator(gPHSPi0,"gPHSPi0",1);//for PHOS

  //return gener;
  return cocktail;
}




void ProcessEnvironmentVars()
{

  // Run number
  if (gSystem->Getenv("DC_RUN")) {
    runNumber = atoi(gSystem->Getenv("DC_RUN"));
  }

  // Run type
  if (gSystem->Getenv("CONFIG_RUN_TYPE")) {
    for (Int_t iRun = 0; iRun < kRunMax; iRun++) {
      if (strcmp(gSystem->Getenv("CONFIG_RUN_TYPE"), pprRunName[iRun])==0) {
	proc = (PDC06Proc_t)iRun;
      }
    }
  }

  // Field
  if (gSystem->Getenv("CONFIG_FIELD")) {
    for (Int_t iField = 0; iField < kFieldMax; iField++) {
      if (strcmp(gSystem->Getenv("CONFIG_FIELD"), pprField[iField])==0) {
	mag = (Mag_t)iField;
	cout<<"Field set to "<<pprField[iField]<<endl;
      }
    }
  }

  // Energy
  if (gSystem->Getenv("CONFIG_ENERGY")) {
    energy = atoi(gSystem->Getenv("CONFIG_ENERGY"));
  }
  if (energy>0) cout<<"Energy set to "<<energy<<" GeV"<<endl;
  else SetEnergyFromGRP();

  // Random Number seed
  if (gSystem->Getenv("CONFIG_SEED")) {
    seed = atoi(gSystem->Getenv("CONFIG_SEED"));
  }

}

void SetEnergyFromGRP()
{
  // obtain energy from GRP
  printf("Extracting beam energy from GRP for run %d\n",runNumber);
  if (runNumber<1) {
    printf("Cannot extract energy from GRP for unphysical run %d\n",runNumber);
    exit(1);
  }
  AliCDBEntry* entry = AliCDBManager::Instance()->Get("GRP/GRP/Data");
  AliGRPObject* grpData = dynamic_cast<AliGRPObject*>(entry->GetObject()); 
  energy = grpData->GetBeamEnergy() * 2.;
  printf("CMS Energy set to %.1f GeV from GRP per charge energy %.1f\n",energy,grpData->GetBeamEnergy());
}

AliGenerator * GenParamCalo(Int_t nPart, Int_t type, TString calo) {
   // nPart of type (Pi0, Eta, Pi0Flat, EtaFlat, ...) in EMCAL or PHOS
   // CAREFUL EMCAL year 2011 configuration
   AliGenParam *gener = new AliGenParam(nPart,new AliGenPHOSlib(),type,"");

   // meson cuts
   gener->SetMomentumRange(0,999);

   if(calo=="EMCAL") {
      //meson acceptance
      gener->SetYRange(-0.8,0.8);
      gener->SetPtRange(2,50);
      // photon cuts
      gener->SetForceDecay(kGammaEM); // Ensure the decays are photons
      gener->SetCutOnChild(1);
      gener->SetChildPtRange(0.,30);
      gener->SetPhiRange(80., 180.); // year 2011
      gener->SetThetaRange(EtaToTheta(0.7),EtaToTheta(-0.7));
      //decay acceptance
      gener->SetChildThetaRange(EtaToTheta(0.7),EtaToTheta(-0.7));
      gener->SetChildPhiRange(80., 180.); // year 2011
   } else if(calo=="PHOS") {
      gener->SetYRange(-0.15,0.15);
      gener->SetPhiRange(240., 330.);// year 2015
      gener->SetPtRange(0.3,80);
   }

   return gener;

}
