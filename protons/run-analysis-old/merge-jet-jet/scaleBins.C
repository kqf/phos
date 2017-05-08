void ScaleMergedExample(Int_t bin = -1, TString filename = "Merged", TString folder = "HistogramFolder" )
{
  if (bin <= 0)  for (Int_t i = 1; i < 11; i++) ForBin(i);
  else ForBin(bin, opt, tm);
}

void ForBin(Int_t bin = 1, TString filename = "Merged", TString folder = "HistogramFolder")
{
  //printf("Scale bin %d\n",bin);

  // TODO: Tune it for my input

  TFile * f = TFile::Open(Form("%d/%s.root", bin, filename.Data()), "read");
  TList* list = (TList*) f->Get(folder);

  if (!list)
  {
    printf("No list available \n");
    return;
  }

  Int_t nEvents = ((TH1F*)list->FindObject("hNEvents"))->GetEntries();
  //printf("N events %e %s\n",nEvents, opt.Data());
  TObject * h ;

// Set directly the cross section for production LHC12a2f
//  Double_t scaleBin[] = {
//    4.37e+00 , // Bin 0 : 0-5 GeV
//    4.33e+00 , // Bin 1 : 5-11 GeV
//    5.21e-01 , // Bin 2 : 11-21 GeV
//    4.15e-02 , // Bin 3 : 21-36 GeV
//    4.01e-03 , // Bin 4 : 36-57 GeV
//    4.59e-04 , // Bin 5 : 57-84 GeV
//    6.55e-05 , // Bin 6 : 84-117 GeV
//    1.05e-05 , // Bin 7 : 117-152 GeV
//    2.31e-06 , // Bin 8 : 152-191 GeV
//    5.80e-07 , // Bin 9 : 191-234 GeV
//    2.08e-07 , // Bin 10: > 234 GeV
//  };

//  Double_t scale = scaleBin[bin]/nEvents ;
//  printf("xs per event %e, xe nevents %e \n",scaleBin[bin],scale);

  // Extract the cross section from the corresponding histograms in the file
  TH1F* hScale = (TH1F *) list->FindObject("hScaleFactor");
  Int_t nmerged  = hScale->GetEntries();
  Double_t scaleF = hScale->GetBinContent(1);

  printf("Bin %d, scale %e \n", bin, scaleF / nmerged);

  Double_t scale = scaleF / nmerged / nEvents ;

  printf("\t scaling ...\n ");

  for (Int_t i = 0; i < list->GetEntries(); i++)
  {
    h = list->At(i);
    if (h)
    {
      if ( !strncmp(h->ClassName(), "TH", 2) )
      {
        //snprintf(name, buffersize, "%sScaled", h->GetName()) ;

        TH1 * hout = dynamic_cast<TH1*> (h);//(h->Clone(name)) ;

        if (hout)
        {
          hout->Sumw2();
          hout->Scale(scale) ;
        }
      }
    }
  }

  printf("\t ... end scaling, write ...\n");
  TFile * fout = new TFile(Form("%d/Scaled.root", bin), "recreate");

  fout->Print("");

  list->Write();

  fout->Close();
  delete fout;
  f->Close();
  delete f;
  delete h;
  delete hScale;
  printf("\t ... done.\n");


}