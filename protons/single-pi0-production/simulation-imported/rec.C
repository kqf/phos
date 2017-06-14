void rec()
{
	AliReconstruction reco;

	//
	// switch off cleanESD, write ESDfriends and Alignment data
	// reco.SetRunReconstruction("ITS TOF PHOS HMPID MUON PMD T0 VZERO FMD");
	//reco.SetRunReconstruction("ALL -EMCAL");
	reco.SetRunReconstruction("PHOS");

	reco.SetCleanESD(kFALSE);
	reco.SetStopOnError(kFALSE);
	reco.SetWriteESDfriend();
	reco.SetWriteAlignmentData();
	reco.SetFractionFriends(.1);

	reco.SetRunPlaneEff(kTRUE);
	reco.SetUseTrackingErrorsForAlignment("ITS");

	// RAW OCDB
	reco.SetDefaultStorage("alien://Folder=/alice/data/2015/OCDB");



	/*

		// ITS (2 objects)

		reco.SetSpecificStorage("ITS/Align/Data",     "alien://folder=/alice/simulation/2008/v4-15-Release/Residual");
		reco.SetSpecificStorage("ITS/Calib/SPDSparseDead", "alien://folder=/alice/simulation/2008/v4-15-Release/Residual");

		// MUON objects (1 object)

		reco.SetSpecificStorage("MUON/Align/Data","alien://folder=/alice/simulation/2008/v4-15-Release/Residual");

		// TPC (7 objects)

		//
		// TPC (2 new objects for Run2 MC)

	        // Parameters should be used from the raw OCDB at some point
		reco.SetSpecificStorage("TPC/Calib/Parameters",     "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
	        // ClusterParam needs to be tuned for each group of MCs
		reco.SetSpecificStorage("TPC/Calib/ClusterParam",   "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
		reco.SetSpecificStorage("TPC/Calib/RecoParam",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Full/");

		// TPC (4 old objects)
		reco.SetSpecificStorage("TPC/Align/Data",           "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
		reco.SetSpecificStorage("TPC/Calib/TimeGain",       "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
		reco.SetSpecificStorage("TPC/Calib/TimeDrift",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
		reco.SetSpecificStorage("TPC/Calib/Correction",     "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");

	        // ZDC
	        reco.SetSpecificStorage("ZDC/Align/Data","alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
		reco.SetSpecificStorage("ZDC/Calib/Pedestals",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
		// TOF (Pb-Pb anchored on pp)
		//	reco.SetSpecificStorage("TOF/Calib/RecoParam",       "alien://Folder=/alice/cern.ch/user/m/morsch/pbpb2015/");
		//	reco.SetSpecificStorage("TOF/Calib/RecoParam",        "alien://Folder=/alice/data/2011/OCDB");


	*/

	reco.SetRunQA(":");
	reco.Run();
}
