#ifndef TENDER_H
#define TENDER_H

AliPHOSTenderTask * AddPHOSTender(Bool_t isMC, TString & msg)
{
    TString decalibration = "Run2Tune";
    AliPHOSTenderTask * tender = AddAODPHOSTender(
        "PHOSTenderTask",  // Task Name
        "PHOStender",      // Container Name
        decalibration,     // Important: de-calibration
        1,                 // Important: reco pass
        isMC               // Important: is MC?
     );

    AliPHOSTenderSupply * supply = tender->GetPHOSTenderSupply();
    supply->ForceUsingBadMap("../../datasets/BadMap_LHC16-updated.root");

    TString nonlinearity = isMC ? "Run2TuneMC": "Run2Tune";
    supply->SetNonlinearityVersion(nonlinearity);  

    if (isMC)
    {
        // Important: Keep track of this variable
        // ZS threshold in unit of GeV
        Double_t zs_threshold = 0.020;
        supply->ApplyZeroSuppression(zs_threshold);
    }

    msg += " with tender option: ";
    msg += decalibration;
    msg += ", Nonlinearity version: ";
    msg += nonlinearity;
    return tender;
}

#endif
