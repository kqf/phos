void saveAsImage(TString path = "LHC16k", TString filename = "000256619.root")
{
	gROOT->SetBatch(kTRUE);
	gStyle->SetOptStat(kFALSE);
	
	TString run = extractRunNumber(filename);
	cout << "Trying to read " << path + "/" + filename << endl ;
	TFile * input = new TFile(path + "/" + filename, "read");

	TCanvas * canvas = new TCanvas(run, run, 800, 800);
	canvas->Divide(2, 2);
	TList * histograms = input->Get("HeatMaps");
	for(Int_t i = 0; i < histograms->GetEntries(); ++i)
	{
		TH1 * histogram = histograms->At(i);
		canvas->cd(i + 1);
		histogram->Draw("colz");
	}

	canvas->cd();
	TText t(0.25, 0.49, Form("Fired cells in selected clusters for run %s", (const char *) run) );
	t.SetTextSize(0.03);
	if (run.Atoi() >  256944 && run.Atoi() < 257145) t.SetTextColor(48);
	t.Draw();

	canvas->SaveAs(path + "/" + run + ".pdf");
}

TString extractRunNumber(TString f)
{
	TString res(f(0, f.Length() - 5)); 
	return Form("%d", res.Atoi());
}