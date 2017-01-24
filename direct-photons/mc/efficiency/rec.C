void rec()//(const char *filename="raw.root")
{
  /////////////////////////////////////////////////////////////////////////////////////////
  //
  // Reconstruction script for 2010 RAW data
  //
  /////////////////////////////////////////////////////////////////////////////////////////

  
  // Set the CDB storage location
   // AliCDBManager::Instance()->SetDefaultStorage("raw://");
   AliCDBManager * man = AliCDBManager::Instance();

     man->SetDefaultStorage("local://OCDBdrain/alice/data/2010/OCDB");


  AliReconstruction reco;

  // Set reconstruction flags (skip detectors here if neded with -<detector name>

  reco.SetRunReconstruction("PHOS, ITS, TPC");


  reco.SetRunQA(":") ;
  reco.SetQARefDefaultStorage("local://$ALICE_ROOT/QAref") ;

  // AliReconstruction settings
  reco.SetWriteESDfriend(kTRUE);
  //rec.SetInput(filename);

  // Special ZDC reco param.
 // reco.SetRecoParam("ZDC",AliZDCRecoParamPbPb::GetHighFluxParam(7000)); 

  // Write out 2% of ESD friends 
  reco.SetFractionFriends(0.01);

  // switch off cleanESD
 // reco.SetCleanESD(kFALSE);

  //Ignore SetStopOnError
  reco.SetStopOnError(kFALSE);

  AliLog::Flush();
  reco.Run();

}


