AliAnalysisGrid* CreateAlienHandler()
{
  // source /tmp/gclient_env_$UID in the current shell.
  // if (!AliAnalysisGrid::CreateToken()) return NULL;

  AliAnalysisAlien *plugin = new AliAnalysisAlien();
  plugin->SetOverwriteMode();
  // Set the run mode (can be "full", "test", "offline", "submit" or "terminate")
  plugin->SetRunMode("full");
 
  plugin->SetAPIVersion("V1.1x");
  plugin->SetAliPhysicsVersion("vAN-20160522-1");
  plugin->SetCheckCopy(kFALSE);
 
  plugin->SetGridDataDir("/alice/data/2010/LHC10e");
  plugin->SetDataPattern("*/pass4/AOD/*AOD.root");
  
  plugin->SetRunPrefix("000");   // real data

  plugin->AddRunNumber(130850);
  plugin->AddRunNumber(130848);
  plugin->AddRunNumber(130847);
  plugin->AddRunNumber(130844);
  plugin->AddRunNumber(130842);
  //plugin->AddRunNumber(130840);//log book entry as bad, NO AOD filter
  //  plugin->AddRunNumber(130834);//NO AOD filter
  plugin->AddRunNumber(130804);
  plugin->AddRunNumber(130803);
  plugin->AddRunNumber(130802);
  plugin->AddRunNumber(130799);
  plugin->AddRunNumber(130798);
  plugin->AddRunNumber(130795);
  plugin->AddRunNumber(130793);
  plugin->AddRunNumber(130704);
  plugin->AddRunNumber(130696);
  // plugin->AddRunNumber(130628);//NO AOD filter
  // plugin->AddRunNumber(130608);// too noisy log book
  // plugin->AddRunNumber(130601);// too noisy log book
  plugin->AddRunNumber(130526);
  //plugin->AddRunNumber(130524);
  plugin->AddRunNumber(130520);
  plugin->AddRunNumber(130519);
  //  plugin->AddRunNumber(130517);
  plugin->AddRunNumber(130481);
  plugin->AddRunNumber(130480);
  //  plugin->AddRunNumber(130479);//bad qa lumi scan
  plugin->AddRunNumber(130343);
  plugin->AddRunNumber(130342);//bad qa
  plugin->AddRunNumber(130179);//bad qa
  // plugin->AddRunNumber(130178);
  //  plugin->AddRunNumber(130172);
  plugin->AddRunNumber(130168);
  //  plugin->AddRunNumber(130158);
  plugin->AddRunNumber(130157);///////////////
  plugin->AddRunNumber(130151);
  // plugin->AddRunNumber(130149);
  plugin->AddRunNumber(130148);
  // plugin->AddRunNumber(129983);
  // plugin->AddRunNumber(129966);
  plugin->AddRunNumber(129962);
  plugin->AddRunNumber(129961);
  plugin->AddRunNumber(129960);
  plugin->AddRunNumber(129959);
  plugin->AddRunNumber(129748);
  plugin->AddRunNumber(129744);
  plugin->AddRunNumber(129742);
  plugin->AddRunNumber(129738);
  plugin->AddRunNumber(129736);
  plugin->AddRunNumber(129735);
  plugin->AddRunNumber(129734);
  plugin->AddRunNumber(129729);
  plugin->AddRunNumber(129726);
  plugin->AddRunNumber(129725);
  plugin->AddRunNumber(129723);
  plugin->AddRunNumber(129667);
  //  plugin->AddRunNumber(129666);
  plugin->AddRunNumber(129659);
  //plugin->AddRunNumber(129654);
  plugin->AddRunNumber(129653);
  plugin->AddRunNumber(129652);
  plugin->AddRunNumber(129651);
  plugin->AddRunNumber(129650);
  plugin->AddRunNumber(129647);
  plugin->AddRunNumber(129641);
  plugin->AddRunNumber(129639);
  plugin->AddRunNumber(129599);
  plugin->AddRunNumber(129587);
  plugin->AddRunNumber(129586);
  // plugin->AddRunNumber(129540);
  plugin->AddRunNumber(129536);
  plugin->AddRunNumber(129528);
  plugin->AddRunNumber(129527);
  plugin->AddRunNumber(129525);
  plugin->AddRunNumber(129524);
  plugin->AddRunNumber(129523);//
  plugin->AddRunNumber(129521);
  plugin->AddRunNumber(129520);//
  plugin->AddRunNumber(129519);
  plugin->AddRunNumber(129516);
  plugin->AddRunNumber(129515);
  plugin->AddRunNumber(129514);
  plugin->AddRunNumber(129513);
  // plugin->AddRunNumber(129042);//bad qa
  // plugin->AddRunNumber(129041);//bad qa
  plugin->AddRunNumber(128913);
  plugin->AddRunNumber(128912);//log book entry as bad
  plugin->AddRunNumber(128911);//log book entry as bad
  plugin->AddRunNumber(128855);
  //  plugin->AddRunNumber(128853);
  //  plugin->AddRunNumber(128850);
  //  plugin->AddRunNumber(128843);
  //  plugin->AddRunNumber(128836);
  plugin->AddRunNumber(128835);
  plugin->AddRunNumber(128834);//log book
  // plugin->AddRunNumber(128833);
  //  plugin->AddRunNumber(128824);
  // plugin->AddRunNumber(128823);
  plugin->AddRunNumber(128820);
  plugin->AddRunNumber(128819);
  plugin->AddRunNumber(128813);//bad qa
  plugin->AddRunNumber(128778);
  plugin->AddRunNumber(128777);
  plugin->AddRunNumber(128678);
  plugin->AddRunNumber(128677);
  plugin->AddRunNumber(128621);
  plugin->AddRunNumber(128615);
  plugin->AddRunNumber(128611);
  plugin->AddRunNumber(128609);
  // plugin->AddRunNumber(128605);
  plugin->AddRunNumber(128596);
  plugin->AddRunNumber(128594);
  plugin->AddRunNumber(128592);
  plugin->AddRunNumber(128590);
  plugin->AddRunNumber(128582);
  plugin->AddRunNumber(128507);
  plugin->AddRunNumber(128506);
  plugin->AddRunNumber(128505);
  plugin->AddRunNumber(128504);
  plugin->AddRunNumber(128503);
  plugin->AddRunNumber(128498);
  plugin->AddRunNumber(128495);
  plugin->AddRunNumber(128494);
  plugin->AddRunNumber(128486);
  plugin->AddRunNumber(128483);
  //  plugin->AddRunNumber(128452);//0%
  plugin->AddRunNumber(128366);
  plugin->AddRunNumber(128263);
  plugin->AddRunNumber(128260);
  plugin->AddRunNumber(128257);
  plugin->AddRunNumber(128053);//bad qa
  plugin->AddRunNumber(128050);//bad qa
  plugin->AddRunNumber(127942);
  plugin->AddRunNumber(127941);
  plugin->AddRunNumber(127940);///////////
  plugin->AddRunNumber(127937);
  plugin->AddRunNumber(127936);
  plugin->AddRunNumber(127935);
  plugin->AddRunNumber(127933);
  plugin->AddRunNumber(127932);
  plugin->AddRunNumber(127931);
  plugin->AddRunNumber(127930);
  plugin->AddRunNumber(127822);
  plugin->AddRunNumber(127819);
  plugin->AddRunNumber(127817);
  plugin->AddRunNumber(127815);
  plugin->AddRunNumber(127814);
  plugin->AddRunNumber(127813);
  plugin->AddRunNumber(127730);
  plugin->AddRunNumber(127729);
  plugin->AddRunNumber(127724);
  plugin->AddRunNumber(127719);
  plugin->AddRunNumber(127718);
  plugin->AddRunNumber(127714);
  plugin->AddRunNumber(127712);
  
  plugin->SetNrunsPerMaster(1);
  plugin->SetOutputToRunNo();
  plugin->SetMergeViaJDL();
  
  plugin->SetGridWorkingDir("2010/EbyPv1/LHC10eAOD_recalib");
  plugin->SetGridOutputDir("Output"); 
  
  plugin->SetAnalysisSource("AliAnalysisTaskEpRatiopp.cxx");
  plugin->AddIncludePath("-I$ROOTSYS/include -I$ALICE_ROOT -I$ALICE_ROOT/include -I$ALICE_PHYSICS -I$ALICE_PHYSICS/include -I$ALICE_ROOT/ITS -I$ALICE_ROOT/TPC -I$ALICE_ROOT/CONTAINERS -I$ALICE_ROOT/STEER/STEER -I$ALICE_ROOT/STEER/STEERBase -I$ALICE_ROOT/STEER/ESD -I$ALICE_ROOT/STEER/AOD -I$ALICE_ROOT/TRD -I$ALICE_PHYSICS/macros -I$ALICE_PHYSICS/ANALYSIS -I$ALICE_PHYSICS/OADB -I$ALICE_PHYSICS/PWGGA -I$ALICE_PHYSICS/PHOS -g");
  
  plugin->SetAdditionalLibs(" libTree.so libGeom.so libVMC.so libXMLIO.so libMatrix.so "
                            " libPhysics.so libMinuit.so libSTEERBase.so libGui.so "
                            " libCDB.so libESD.so libAOD.so libRAWDatabase.so libProof.so "
                            " libOADB.so libANALYSIS.so libSTEER.so libRAWDatarec.so "
                            " libRAWDatasim.so libVZERObase.so libVZEROrec.so libEMCALUtils.so "
                            " libEMCALraw.so libEMCALbase.so libEMCALsim.so libEMCALrec.so "
                            " libPHOSUtils.so libPHOSbase.so libPHOSsim.so libPHOSrec.so "
                            " libPHOSshuttle.so libANALYSISalice.so libPWGCaloTrackCorrBase.so "
                            " libPWGGACaloTrackCorrelations.so libPWGGAEMCALTasks.so "
                            " libPWGGAGammaConv.so libPWGGAPHOSTasks.so libPHOSpi0Calib.so "
			    " libTender.so libTenderSupplies.so "
                            " AliAnalysisTaskEpRatiopp.cxx AliAnalysisTaskEpRatiopp.h ");
			   

  plugin->SetDefaultOutputs();
  plugin->SetAnalysisMacro("AN.C");
  plugin->SetSplitMaxInputFileNumber(500);
  plugin->SetExecutable("AnaEbyP.sh");
  plugin->SetMasterResubmitThreshold(90);
  plugin->SetTTL(48000);
  plugin->SetInputFormat("xml-single");
  plugin->SetJDLName("AN.jdl");
  plugin->SetPrice(1);    
  plugin->SetNtestFiles(1);
  plugin->SetSplitMode("se");
  plugin->SetKeepLogs();
  plugin->SetRegisterExcludes("EventStat_temp.root event_stat.root");
  return plugin;
}
