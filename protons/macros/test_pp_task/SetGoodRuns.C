#include <vector>
#include <TString.h>

void SetGoodRuns(AliAnalysisAlien *plugin, TString type, TString period, TString pass, TString MCname = "", Int_t pThardbin=-1)
{
  TString DataDir     = "";
  TString DataPattern = "";
  Int_t year = -1;
  vector<Int_t> vrun;

  //add your good runs->
  if(period.Contains("LHC15n")){
    Int_t run[] = {
      244628, 244627, 244618, 244617, 244542, 244540, 244531, 244484, 244483, 244482,
      244481, 244480, 244453, 244421, 244418, 244416, 244411,
      244377, 244364, 244359, 244355, 244351, 244343, 244340//low IR
    };

    const Int_t Nrun = sizeof(run)/sizeof(run[0]);
    for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
  }
  else if(period.Contains("LHC15o")){
    if(MCname==""){
      if(pass=="pass1"){
        //plugin->AddRunNumber(246540);//poor statistics.
        //group1
        //Int_t run[] = {
        //  246982, 246980, 246937, 246930, 246928, 246867, 246865, 246855, 246851, 246847,
        //  246846, 246845, 246844, 246810, 246809, 246808, 246807, 246805, 246804, 246766,
        //  246765, 246763, 246760, 246759, 246758, 246757, 246751, 246750, 246676, 246675,
        //  246495, 246493, 246488, 246487, 246434, 246431, 246428, 246424
        //};
        ////group2
        //Int_t run[] = {
        //  246275, 246271, 246225, 246222, 246217, 246185, 246182, 246181, 246180, 246178,
        //  246153, 246152, 246151, 246148, 246115, 246113, 246089, 246087, 246049, 246048,
        //  246042, 246037, 246036, 246012, 246003, 246001, 245963, 245954, 245952, 245949,
        //  245923, 245831, 245829, 245705, 245702, 245700, 245692, 245683
        //};
        //all 76 good runs
        Int_t run[] = {
          246982, 246980, 246937, 246930, 246928, 246867, 246865, 246855, 246851, 246847,
          246846, 246845, 246844, 246810, 246809, 246808, 246807, 246805, 246804, 246766,
          246765, 246763, 246760, 246759, 246758, 246757, 246751, 246750, 246676, 246675,
          246495, 246493, 246488, 246487, 246434, 246431, 246428, 246424, 246275, 246271,
          246225, 246222, 246217, 246185, 246182, 246181, 246180, 246178, 246153, 246152,
          246151, 246148, 246115, 246113, 246089, 246087, 246049, 246048, 246042, 246037,
          246036, 246012, 246003, 246001, 245963, 245954, 245952, 245949, 245923, 245831,
          245829, 245705, 245702, 245700, 245692, 245683
        };
        const Int_t Nrun = sizeof(run)/sizeof(run[0]);
        for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
      }
      else if(pass=="pass1_pidfix"){
        //plugin->AddRunNumber(245411);//centrality is suspicious.
        Int_t run[] = {
          245545, 245544, 245543, 245542, 245540, 245535, 245507, 245505, 245504, 245501,
          245497, 245496, 245454, 245453, 245452, 245450, 245446, 245441, 245439, 245410,
          245409, 245407, 245401, 245397, 245396, 245353, 245349, 245347, 245346, 245345,
          245343, 245259, 245233, 245232, 245231, 245152, 245151, 245146, 245145
        };
        const Int_t Nrun = sizeof(run)/sizeof(run[0]);
        for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
      }
      else if(pass.Contains("lowIR")){
        Int_t run[] = {
          246392, 246391, 246390, 245068, 245066, 245064, 244983, 244982, 244980,
          244975, 244918
        };
        const Int_t Nrun = sizeof(run)/sizeof(run[0]);
        for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
      }
    }
    else if(MCname.Contains("LHC16g1")){//general purpose MC anchored to LHC15o (LHC16g1[abc])
      //this production has all runs.
      //note that no ZDC in 245148 and 245061
      Int_t run[] = {
        246982, 246980, 246937, 246930, 246928, 246867, 246865, 246855, 246851, 246847,
        246846, 246845, 246844, 246810, 246809, 246808, 246807, 246805, 246804, 246766,
        246765, 246763, 246760, 246759, 246758, 246757, 246751, 246750, 246676, 246675,
        246495, 246493, 246488, 246487, 246434, 246431, 246428, 246424, 246275, 246271,
        246225, 246222, 246217, 246185, 246182, 246181, 246180, 246178, 246153, 246152,
        246151, 246148, 246115, 246113, 246089, 246087, 246049, 246048, 246042, 246037,
        246036, 246012, 246003, 246001, 245963, 245954, 245952, 245949, 245923, 245831,
        245829, 245705, 245702, 245700, 245692, 245683,

        245545, 245544, 245543, 245542, 245540, 245535, 245507, 245505, 245504, 245501,
        245497, 245496, 245454, 245453, 245452, 245450, 245446, 245441, 245439, 245410,
        245409, 245407, 245401, 245397, 245396, 245353, 245349, 245347, 245346, 245345,
        245343, 245259, 245233, 245232, 245231, 245152, 245151, 245146, 245145,

        246392, 246391, 246390, 245068, 245066, 245064, 244983, 244982, 244980,
        244975, 244918
      };
      const Int_t Nrun = sizeof(run)/sizeof(run[0]);
      for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
    }
    else if(MCname.Contains("LHC17i7")){//general purpose MC anchored to LHC15o (LHC16g1[abc])
      //this production has all runs.
      //note that no ZDC in 245148 and 245061
      Int_t run[] = { 246980, 246488 };
      const Int_t Nrun = sizeof(run)/sizeof(run[0]);
      for(Int_t i=0;i<Nrun;i++) vrun.push_back(run[i]);
    }
  }//end of LHC15o




  //<-add your good runs

  if(MCname == ""){//for real data
    if(period.Contains("LHC15"))      year = 2015;
    else if(period.Contains("LHC16")) year = 2016;
    else if(period.Contains("LHC17")) year = 2017;
    else if(period.Contains("LHC18")) year = 2018;
  }
  else if(MCname.Contains("LHC15")) year = 2015;
  else if(MCname.Contains("LHC16")) year = 2016;
  else if(MCname.Contains("LHC17")) year = 2017;
  else if(MCname.Contains("LHC18")) year = 2018;

  if(MCname=="") DataDir = Form("/alice/data/%d/%s/",year,period.Data());
  else{
    if(pThardbin > 0) DataDir = Form("/alice/sim/%d/%s/%d/" ,year,MCname.Data(),pThardbin);
    else              DataDir = Form("/alice/sim/%d/%s/" ,year,MCname.Data());
  }
  if(MCname==""){//for real data
    if(type.Contains("ESD"))      DataPattern = Form("/%s/*/AliESDs.root",pass.Data());
    //else if(type.Contains("AOD")) DataPattern = Form("/%s/%s/*/AliAOD.root" ,pass.Data(),type.Data());//merged AOD.//AOD186,AOD123 are also available.
    else if(type.Contains("AOD")) DataPattern = Form("/%s/*/AliAOD.root" ,pass.Data());//AOD
  }
  else{//for M.C.
    if(type.Contains("ESD"))      DataPattern = Form("/*/AliESDs.root");
    //else if(type.Contains("AOD")) DataPattern = Form("/%s/*/AliAOD.root" ,type.Data());//merged AOD.//AOD186,AOD123 are also available.
    else if(type.Contains("AOD")) DataPattern = Form("/*/AliAOD.root");//non-merged AOD.
  }

  printf("DataDir = %s , DataPettern = %s\n",DataDir.Data(),DataPattern.Data());

  plugin->SetGridDataDir(DataDir);
  plugin->SetDataPattern(DataPattern);
  if(MCname=="") plugin->SetRunPrefix("000");//for real data

  const Int_t Nrun = vrun.size();
  if(MCname=="") plugin->SetNrunsPerMaster(1);
  else{
    if(pThardbin > 0) plugin->SetNrunsPerMaster(Nrun);
    else              plugin->SetNrunsPerMaster(1);
  }

  printf("A run list of %s %s contains %d runs : ",period.Data(),pass.Data(),Nrun);
  for(Int_t irun=0;irun<Nrun;irun++){
    printf(" %d ",vrun[irun]);
    plugin->AddRunNumber(vrun[irun]);
  }
  printf("\n");

  vrun.clear();
}

