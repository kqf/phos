void MakeTrendingPHOSQA(const char * path = "", const char * file = "QAresults.root", Int_t runNumber, Bool_t IsOnGrid = kFALSE)
{
  //const char* dirNames[] = {"PHOSCellsQA_AnyInt","PHOSCellsQA_PHI7","PHOSPbPbQAResults","PHOSTriggerQAResults"};

  TFile * fin = TFile::Open(TString(path) + file);
  if (!fin) {printf("Cannot open file %s. exit.\n", file); return; }

  const char * listNameAnyInt = "PHOSCellsQA";
  TObjArray * listAnyInt = (TObjArray *)fin->Get(listNameAnyInt);

  TFile * trendFile = new TFile(Form("%strending%d.root", path, runNumber), "recreate");
  Float_t emin = 0.3, emax = 1000.; // minimum and maximum energy of the cluster
  TTree * ttree = new TTree("trending", Form("(%.2f < E < %.0f)", emin, emax));

  const int nmods = 4;
  Int_t   nEvents = 0;
  Float_t avCluEnergySM[nmods]   = { -9999., -9999., -9999., -9999.};
  Float_t avCluMultSM[nmods]     = { -9999., -9999., -9999., -9999.};
  Float_t avNcellPerCluSM[nmods] = { -9999., -9999., -9999., -9999.};


  ttree->Branch("run", &runNumber, "run/I");
  ttree->Branch("nEvents", &nEvents, "nEvents/F");

  for (Int_t i = 0; i < nmods; ++i)
  {
    ttree->Branch(Form("avCluEnergySM%d", i + 1), &avCluEnergySM[i], Form("avCluEnergySM%d/F", i + 1) );
    ttree->Branch(Form("avCluMultSM%d", i + 1), &avCluMultSM[i], Form("avCluMultSM%d/F", i + 1) );
    ttree->Branch(Form("avNcellPerCluSM%d", i + 1), &avNcellPerCluSM[i], Form("avNcellPerCluSM%d/F", i + 1) );
  }



  //-------- Number of processed events --------------------------------------------------------------
  TH1 * hNEventsProcessedPerRun = (TH1 *)listAnyInt->FindObject("hNEventsProcessedPerRun");
  // if (hNEventsProcessedPerRun) nEvents =  hNEventsProcessedPerRun->GetEntries();
  if (hNEventsProcessedPerRun) nEvents =  hNEventsProcessedPerRun->GetBinContent(hNEventsProcessedPerRun->FindBin(runNumber));
  //-------- Mean cluster energy, number of cells in the cluster Mean number of clusters per event ---

  TH2 * h;
  for (Int_t i = 0; i < nmods; ++i)
  {
    h = (TH2 *)listAnyInt->FindObject(Form("run%d_hNCellsInClusterSM%d", runNumber, i + 1));

    if (h && nEvents )
    {
      h->GetXaxis()->SetRangeUser(emin, emax);
      avCluEnergySM[i] = h->ProjectionX()->GetMean();
      avNcellPerCluSM[i] = h->ProjectionY()->GetMean();
      avCluMultSM[i] = h->Integral() / nEvents;
    }
  }
  
  //-------- Average pi0s number per event, pi0 mass, width -------------------------------------------
  Double_t nraw, enraw, mass, emass, sigma, esigma;
  Int_t sm;
  TH1 * hm;
  char name[20], leaf[20];

	Float_t avPi0NumSM[nmods]      = {0., 0., 0., 0.};
	Float_t avPi0MassSM[nmods]     = {-9999, -9999, -9999, -9999};
	Float_t avPi0SigmaSM[nmods]    = {-9999, -9999, -9999, -9999};
	Float_t avPi0NumErrSM[nmods]   = {0., 0., 0., 0.};
	Float_t avPi0MassErrSM[nmods]  = {-9999, -9999, -9999, -9999};
	Float_t avPi0SigmaErrSM[nmods] = {-9999, -9999, -9999, -9999};

  for (Int_t i = 0; i < nmods; ++i)
  {
  
	  sm = i + 1;
	  hm = (TH1 *)listAnyInt->FindObject(Form("run%i_hPi0MassSM%iSM%i", runNumber, sm, sm));

	  sprintf(name, "avPi0NumSM%d", sm);
	  sprintf(leaf, "avPi0NumSM%d/F", sm);
	  ttree->Branch(name, &avPi0NumSM[i], leaf);

	  sprintf(name, "avPi0MassSM%d", sm);
	  sprintf(leaf, "avPi0MassSM%d/F", sm);
	  ttree->Branch(name, &avPi0MassSM[i], leaf);

	  sprintf(name, "avPi0SigmaSM%d", sm);
	  sprintf(leaf, "avPi0SigmaSM%d/F", sm);
	  ttree->Branch(name, &avPi0SigmaSM[i], leaf);

	  sprintf(name, "avPi0NumErrSM%d", sm);
	  sprintf(leaf, "avPi0NumErrSM%d/F", sm);
	  ttree->Branch(name, &avPi0NumErrSM[i], leaf);

	  sprintf(name, "avPi0MassErrSM%d", sm);
	  sprintf(leaf, "avPi0MassErrSM%d/F", sm);
	  ttree->Branch(name, &avPi0MassErrSM[i], leaf);

	  sprintf(name, "avPi0SigmaErrSM%d", sm);
	  sprintf(leaf, "avPi0SigmaErrSM%d/F", sm);
	  ttree->Branch(name, &avPi0SigmaErrSM[i], leaf);

	  FitPi0(hm, nraw, enraw, mass, emass, sigma, esigma, sm, runNumber);

	  if (nEvents) avPi0NumSM[i] = nraw / nEvents;
	  avPi0MassSM[i] = mass;
	  avPi0SigmaSM[i] = sigma;
	  if (nEvents) avPi0NumErrSM[i] = enraw / nEvents;
	  avPi0MassErrSM[i] = emass;
	  avPi0SigmaErrSM[i] = esigma;
	}

  //---------------------------------------------------------------------------------------------------

  ttree->Fill();
  trendFile->cd();

  ttree->Write();
  trendFile->Close();

}


//-----------------------------------------------------------------------------------------------------
void FitPi0(TH1 * h, Double_t & nraw, Double_t & enraw,
            Double_t & mass, Double_t & emass,
            Double_t & sigma, Double_t & esigma,
            Int_t sm, Int_t runNumber,
            Double_t emin = 0.05, Double_t emax = 0.3, Int_t rebin = 1)
{
  // Fits the pi0 peak with crystal ball + pol2,
  // fills number of pi0s, mass, width and their errors.
  nraw = enraw = 0;
  mass = emass = 0;
  sigma = esigma = 0;

  gStyle->SetOptFit();

  if (!h) return;
  if (h->GetEntries() == 0) return;

  if (rebin > 1) h->Rebin(rebin);

  TString oldTitle = h->GetTitle();
  h->SetTitle(Form("Pt > 2 GeV, SM%d run %d ", sm, runNumber) + oldTitle);
  gROOT->SetBatch(kTRUE);

  //crystal ball parameters (fixed by hand for EMCAL)
  Double_t alpha = 1.1;  // alpha >= 0
  Double_t n = 2.;       // n > 1

  // CB tail parameters
  Double_t a = pow((n / alpha), n) * TMath::Exp(-alpha * alpha / 2.);
  Double_t b = n / alpha - alpha;

  // integral value under crystal ball with amplitude = 1, sigma = 1
  // (will be sqrt(2pi) at alpha = infinity)
  Double_t nraw11 = a * pow(b + alpha, 1. - n) / (n - 1.) + TMath::Sqrt(TMath::Pi() / 2.) * TMath::Erfc(-alpha / TMath::Sqrt(2.));

  // signal (crystal ball);
  new TF1("cball", Form("(x-[1])/[2] > -%f ?                        \
                          [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2]))    \
                          : [0]*%f*(%f-(x-[1])/[2])^(-%f)", alpha, a, b, n));

  // background
  new TF1("mypol2", "[0] + [1]*(x-0.135) + [2]*(x-0.135)^2", emin, emax);

  // signal + background
  TF1 * fitfun = new TF1("fitfun", "cball + mypol2", emin, emax);
  fitfun->SetParNames("A", "M", "#sigma", "a_{0}", "a_{1}", "a_{2}");
  fitfun->SetLineColor(kRed);
  fitfun->SetLineWidth(2);

  // make a preliminary fit to estimate parameters
  TF1 * ff = new TF1("fastfit", "gaus(0) + [3]");
  ff->SetParLimits(0, 0., h->GetMaximum() * 1.5);
  ff->SetParLimits(1, 0.1, 0.2);
  ff->SetParLimits(2, 0.004, 0.030);
  ff->SetParameters(h->GetMaximum() / 3., 0.135, 0.010, 0.);
  h->Fit(ff, "0QL", "", 0.105, 0.165);

  fitfun->SetParLimits(0, 0., h->GetMaximum() * 1.5);
  fitfun->SetParLimits(1, 0.12, 0.15);
  fitfun->SetParLimits(2, 0.004, 0.030);

  Float_t parval =  ff->GetParameter(1);
  fitfun->SetParameters(ff->GetParameter(0), ff->GetParameter(1), ff->GetParameter(2), ff->GetParameter(3));
  h->Fit(fitfun, "QLR", "");

  // calculate pi0 values
  mass = fitfun->GetParameter(1);
  emass = fitfun->GetParError(1);

  sigma = fitfun->GetParameter(2);
  esigma = fitfun->GetParError(2);

  Double_t A = fitfun->GetParameter(0);
  Double_t eA = fitfun->GetParError(0);

  nraw = nraw11 * A * sigma / h->GetBinWidth(1);
  enraw = nraw * (eA / A + esigma / sigma);

  gPad->SaveAs(Form("fits/SM%d_Run%d.png", sm, runNumber));
  h->SetTitle(oldTitle);

   //c1->SaveAs();


}

