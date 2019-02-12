
void ProcessRun(TSystemFile * file, TString dirname, const char * ext = ".root")
{
    TString fname = file->GetName();
    if (!fname.EndsWith(ext))
        return;
    TFile * originaFile = TFile::Open(dirname + "/" + fname, "read");
    // cout << "Processing " <<  << endl;

    TFile * ofile = TFile::Open(dirname + ".root", "update");
    TList * histTrigL0 = (TList*) originaFile->Get("PHOSTriggerQAResultsL0");
    histTrigL0->Write(fname.ReplaceAll(".root", ""), TObject::kSingleKey);
    ofile->Close();

    histTrigL0 ->Clear();
    originaFile->Close();
}

void merge(const TString  dirname)
{
    TList * files = TSystemDirectory(dirname, dirname).GetListOfFiles();
    for (Int_t i = 0; i < files->GetEntries(); ++i)
    {
        TSystemFile * file = (TSystemFile *) files->At(i);
        ProcessRun(file, dirname);
    }
}
