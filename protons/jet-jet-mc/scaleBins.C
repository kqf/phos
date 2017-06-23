void scaleBins(TString fileToScale = "LHC17f8a_10.root", TString paths = "LHC17f8a_10.root/MCStudyOnlyTender/", TString prefix = "scaled-")
{
	Float_t scaleFactor = ScaleFactor(paths);

	TFile * file = new TFile(fileToScale, "open");
	TList * keys = file->GetListOfKeys();

	for (int i = 0; i < keys->GetEntries(); ++i)
	{
		TKey * key = dynamic_cast<TKey * >(keys->At(i));
		ScaleSelection(prefix + fileToScale, key->ReadObj(), scaleFactor);
	}

}

Float_t ScaleFactor(TString paths)
{

	TString name;
	Int_t step = 0;

	vector<TString> path;

	while (paths.Tokenize(name, step, "/"))
		path.push_back(name);

	if (path.size() != 2)
		return -1;

	TFile * file = new TFile(path[0], "read");
	TList * list = file->Get(path[1]);
	// list->ls();

	TH1F * hXsec = dynamic_cast<TH1F *>(list->FindObject("hXsec"));
	TH1F * hTrials = dynamic_cast<TH1F *>(list->FindObject("hTrials"));


	if (!hXsec || !hTrials)
		return -1;

	if (!Int_t(hTrials->GetBinContent(1)))
		return -1;

	Float_t res =  hXsec->GetBinContent(1) / hTrials->GetBinContent(1);
	file->Close();
	delete file;
	return res;

}

Bool_t ScaleSelection(TString out, TObject * objlist, Float_t scaleFactor)
{
	TList * list = dynamic_cast<TList *>(objlist);

	TH1F * nevents = list->FindObject("EventCounter");
	Int_t nev = nevents->GetBinContent(1);

	for (int i = 0; i < list->GetEntries(); ++i)
	{

		TH1 * hist = dynamic_cast<TH1 * >(list->At(i));
		TString name = hist->GetName();


		if (name.Contains("hXsec") || name.Contains("hTrials"))
			continue;

		Float_t scale = (nev > 0) ? 1. / nev : 1.;
		hist->Scale(scale);

		if (!name.Contains("EventCounter"))
			hist->Scale(scaleFactor);
	}

	TFile file(out, "update");
	list->Write(list->GetName(), TObject::kSingleKey);
	file.Close();

	return kTRUE;
}