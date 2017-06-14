void RecreateGRP(const char* btype = "A-A", float energy = -1);
void sim(Int_t nev = 10000)
{
    AliSimulation simulator;

    //  simulator.SetWriteRawData("ALL","raw.root",kFALSE);
    simulator.SetMakeSDigits("PHOS");
    simulator.SetMakeDigits("PHOS");
    //simulator.SetMakeDigitsFromHits("ITS TPC");

    //simulator.SetMakeSDigits("TRD TOF PHOS HMPID EMCAL MUON ZDC PMD T0 VZERO FMD AD");
    //simulator.SetMakeDigitsFromHits("ITS TPC");




    // can't detect from GRP if HLT was running, off for safety now
    // simulator.SetRunHLT("");
    //
    //
    // RAW OCDB
    simulator.SetDefaultStorage("alien://Folder=/alice/data/2015/OCDB");
    // Specific storages = 23

    //simulator.SetSpecificStorage("PHOS/Align/Data","local:///Users/Daiki/OCDB/");
    //simulator.SetSpecificStorage("PHOS/Align/Data","alien://Folder=/alice/cern.ch/user/d/dsekihat/simulation/SinglePi0_misalignment/OCDB/");
    //simulator.SetSpecificStorage("PHOS/Align/Data","alien:///alice/cern.ch/user/d/dsekihat/simulation/SinglePi0_misalignment/OCDB/");

    /*

        //
        // ITS  (2 Total)
        //     Alignment from Ideal OCDB

        simulator.SetSpecificStorage("ITS/Align/Data",  "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal");
        simulator.SetSpecificStorage("ITS/Calib/SPDSparseDead",  "alien://Folder=/alice/simulation/2008/v4-15-Release/Full");
        //
        // MUON (1 object)

        simulator.SetSpecificStorage("MUON/Align/Data","alien://folder=/alice/simulation/2008/v4-15-Release/Ideal");

        //
        // TPC (2 new objects for Run2 MC)

            // Parameters should be used from the raw OCDB at some point
        simulator.SetSpecificStorage("TPC/Calib/Parameters",     "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
            // ClusterParam needs to be tuned for each group of MCs
        simulator.SetSpecificStorage("TPC/Calib/ClusterParam",   "alien://Folder=/alice/simulation/2008/v4-15-Release/Residual/");
        simulator.SetSpecificStorage("TPC/Calib/RecoParam",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Full/");

        // TPC (4 old objects)

        simulator.SetSpecificStorage("TPC/Calib/TimeGain",       "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
        simulator.SetSpecificStorage("TPC/Calib/Correction",     "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
        simulator.SetSpecificStorage("TPC/Align/Data",           "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
        simulator.SetSpecificStorage("TPC/Calib/TimeDrift",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");

        // TOF (Pb-Pb anchored on pp)
        // simulator.SetSpecificStorage("TOF/Calib/RecoParam",       "alien://Folder=/alice/cern.ch/user/m/morsch/pbpb2015");
        // ZDC
            simulator.SetSpecificStorage("ZDC/Align/Data", "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");
        simulator.SetSpecificStorage("ZDC/Calib/Pedestals",      "alien://Folder=/alice/simulation/2008/v4-15-Release/Ideal/");

    */


    // Vertex and magfield

    simulator.UseVertexFromCDB();
    simulator.UseMagFieldFromGRP();

    // PHOS simulation settings
    AliPHOSSimParam *simParam = AliPHOSSimParam::GetInstance();
    simParam->SetCellNonLinearity(kFALSE);//switch off cell non-linearity
    //simParam->SetCellNonLineairyA(0.001);
    //simParam->SetCellNonLineairyB(0.2);
    //simParam->SetCellNonLineairyC(1.02);
    // simParam->SetGlobalAltroOffset(1);
    // simParam->SetGlobalAltroThreshold(3);//this should be changed
    // simParam->SetEMCDigitsThreshold(3.0);
    // simParam->SetSampleQualityCut(10);
    //const Double_t APDeff = 0.514*pow(5./22.,2.);//APD PDE * (5mm / 22mm)^2 = 0.02655// default value
    //const Double_t APDeff = 0.4*pow(5./22.,2.);//APD PDE * (5mm / 22mm)^2
    //simParam->SetAPDEfficiency(APDeff);

    //
    // The rest
    //

    simulator.SetRunQA(":");

    printf("Before simulator.Run(nev);\n");
    simulator.Run(nev);
    printf("After simulator.Run(nev);\n");
}


void RecreateGRP(const char* btype, float energy)
{
    //
    TString dcrun = getenv("DC_RUN");
    Int_t run = dcrun.Atoi();
    if (run < 1)
    {
        printf("Failed to extract run number from environment vas RC_RUN: %s", dcrun.Data());
        exit(1);
    }
    // take raw GRP
    AliCDBManager* man = AliCDBManager::Instance();
    if (man->GetLock())
    {
        man->Destroy();
        man = AliCDBManager::Instance();
    }
    man->UnsetDefaultStorage();
    man->SetDefaultStorage("raw://");
    man->SetRun(run);
    AliCDBEntry* grpe = man->Get("GRP/GRP/Data");
    AliGRPObject* grp = (AliGRPObject*)grpe->GetObject();
    //
    // impose beam changes >>
    TString beam = btype;
    if (!beam.IsNull())
    {
        grp->SetBeamType(beam.Data());
        printf("Imposed beam type: %s\n", beam.Data());
    }
    if (energy > 0)
    {
        grp->SetBeamEnergy(energy);
        printf("Imposed beam energy: %13.3f \n", energy);
    }
    // impose beam changes <<
    //
    grpe->SetObject(0);
    AliCDBMetaData* md = new AliCDBMetaData();
    AliCDBId id("GRP/GRP/Data", run, run);
    man->UnsetDefaultStorage();
    man->SetDefaultStorage("local://");
    man->Put(grp, id, md);
    man->UnsetDefaultStorage();
    //
}

