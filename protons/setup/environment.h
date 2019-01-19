void SetupEnvironment()
{
    // ROOT
    gSystem->Load ( "libCore.so" );
    gSystem->Load ( "libGeom.so" );
    gSystem->Load ( "libVMC.so" );
    gSystem->Load ( "libPhysics.so" );
    gSystem->Load ( "libTree.so" );
    gSystem->Load ( "libMinuit.so" );

    // AliROOT
    gSystem->Load ( "libSTEERBase.so" );
    gSystem->Load ( "libESD.so" );
    gSystem->Load ( "libAOD.so" );
    gSystem->Load ( "libANALYSIS.so" );
    gSystem->Load ( "libANALYSISalice.so" );
    gSystem->Load ( "libPWGGAPHOSTasks.so" );

    // Tender
    gSystem->Load("libTender.so");
    gSystem->Load("libTenderSupplies.so");
    gSystem->Load("libPWGGAPHOSTasks.so");

    // for running with root only
    gSystem->Load( "libTree.so" );
    gSystem->Load( "libGeom.so" );
    gSystem->Load( "libVMC.so" );
    gSystem->Load( "libPhysics.so" );

    //add include path
#if !defined (__CINT__) || defined (__CLING__)
    gInterpreter->ProcessLine(".include $ROOTSYS/include");
    gInterpreter->ProcessLine(".include $ALICE_ROOT/include");
#else
    gROOT->ProcessLine(".include $ROOTSYS/include");
    gROOT->ProcessLine(".include $ALICE_ROOT/include");
#endif
}
