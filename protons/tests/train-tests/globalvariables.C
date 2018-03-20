{
TString periodName = "";
TString tenderPassData = "2";
Int_t passNumber = 1;
TString aodConversionCutNumber = "";
TString aodConversionCutNumberOffline = "";
const char *passNameEMC = 0;

/*
//variables set for Gustavo
const char* kPeriod = gSystem->Getenv("ALIEN_JDL_LPMPRODUCTIONTAG"); // needed to recover MC production name or data perio
const char* kProdType = gSystem->Getenv("ALIEN_JDL_LPMPRODUCTIONTYPE"); // MC or dat
const char* kColType = gSystem->Getenv("ALIEN_JDL_LPMINTERACTIONTYPE");  // collision type
Bool_t kMC = kFALSE;
if( !strcmp("MC",kProdType) ) kMC = kTRUE;
//end variables for Gustavo
*/
periodName = "LHC16d";
tenderPassData = "1";
passNumber=1;
aodConversionCutNumber="00000003_06000008400100001000000000";
aodConversionCutNumberOffline="00000003_16000008400100001000000000";
}
