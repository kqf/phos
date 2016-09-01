void ExtractTriggerQA(TString direcotry = "./", Bool_t only_stats = kFALSE)
{
	file = TFile(direcotry + "TriggerQASingle.root");
	TList * inlist = dynamic_cast<TList *>(file.Get("L0"));

	gROOT->LoadMacro("DrawTriggerQA.C");
	for (Int_t i = 0; i < inlist->GetEntries(); ++i)
	{
		if(only_stats) continue;

		TList * run = dynamic_cast<TList *>(inlist->At(i));
		Int_t rnumber = TString(run->GetName()).Atoi();

		DrawTriggerQA(run, "L0", rnumber, direcotry);

		for (int sm = 1; sm < 5; ++sm)
			DrawTriggerQATRU(run, "L0", Form("M%d", sm), rnumber, direcotry);
	}

	if(!only_stats)
	{
		SaveImages(direcotry, "c1"); // Save trigger occupancy
		SaveImages(direcotry, "c2"); // Save trigger occupacy for high energy clusters
	}

	cout << "For run "  << "<Numb>" << fixed << setw(1)  << " " << "TrigCount" << " " << setw(1)<< "<N events>" << endl;
	for (Int_t i = 0; i < inlist->GetEntries(); ++i)
	{
		TList * run = dynamic_cast<TList *>(inlist->At(i));
		TH1 * stat = dynamic_cast<TH1 *>(run->FindObject("hNev"));

		cout.precision(0);
		cout << "For run "  << run->GetName() << fixed << setw(1)  << " " << stat->GetEntries() << " " << setw(1)<< stat->GetBinContent(1) << endl;
	}
}

void SaveImages(TString direcotry, TString cname = "c1")
{
	gStyle->SetOptStat(0);

	Bool_t batch = gROOT->IsBatch();
	gROOT->SetBatch(kTRUE);

	cout << "PROCESSING " << cname << endl;
	TList * data = TFile(direcotry + "ResultsTriggerQA.root", "read").GetListOfKeys();
	for (Int_t i = 0; i < data->GetEntries(); ++i)
	{
		TString name = data->At(i)->GetName();
		cout << "Drawing run " << name <<  " ..." << endl;

		TKey * key = dynamic_cast<TKey *>(data->At(i));
		if (!key) continue;

		TList * run = dynamic_cast<TList *>(key->ReadObj());
		if (!run) continue;

		TCanvas * c1 = dynamic_cast<TCanvas *>(run->FindObject(cname));
		if (!c1) continue;

		c1->Draw();

		TString descr = cname.Contains("c2") ? " high energy clusters" : "";
		TText t(0.35, 0.49, Form("trigger occupancy run %s %s", (const char *) name, (const char *) descr));
		t.SetTextSize(0.03);
		t.Draw();

		TString ctype = cname.Contains("c2") ? "cluster_" : "";
		c1->SaveAs(direcotry + "/images/trigger_occupancy_" + ctype + name + ".pdf");

		delete run;
	}
	gROOT->SetBatch(batch);
}
