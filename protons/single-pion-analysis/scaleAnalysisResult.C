void scaleAnalysisResult(TString fileToScale = "LHC17f8a_10.root", TString prefix = "scaled-")
{
	TFile * file = new TFile(fileToScale, "open");
	TList * keys = file->GetListOfKeys();

	for (int i = 0; i < keys->GetEntries(); ++i)
	{
		TKey * key = dynamic_cast<TKey * >(keys->At(i));
		ScaleSelection(prefix + fileToScale, key->ReadObj());
	}

}


Bool_t ScaleSelection(TString out, TObject * objlist)
{
	TList * list = dynamic_cast<TList *>(objlist);

	TH1F * nevents = list->FindObject("EventCounter");
	Int_t nev = nevents->GetBinContent(1);

	for (int i = 0; i < list->GetEntries(); ++i)
	{

		TH1 * hist = dynamic_cast<TH1 * >(list->At(i));
		TString name = hist->GetName();

		Float_t scale = (nev > 0) ? 1. / nev : 1.;
		hist->Scale(scale);
	}

	TFile file(out, "update");
	list->Write(list->GetName(), TObject::kSingleKey);
	file.Close();

	return kTRUE;
}