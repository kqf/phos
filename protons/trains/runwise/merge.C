
void ProcessRun(TSystemFile * file, const char * ext = ".root")
{
    TString fname = file->GetName();
    if (!file->IsDirectory() && fname.EndsWith(ext))
        cout << fname.Data() << endl;
    cout << "Processing " << file->GetName() << endl;

    TFile * oldRootFile = TFile::Open(run, "read");
    histAnyInt = (TObjArray*)oldRootFile->Get("PHOSCellsQA_AnyInt");
    histPHI7   = (TObjArray*)oldRootFile->Get("PHOSCellsQA_PHI7");
    histTrigL0 = (TList*)oldRootFile->Get("PHOSTriggerQAResultsL0");
    histTrigL1L = (TList*)oldRootFile->Get("PHOSTriggerQAResultsL1Low");
    histTrigL1M = (TList*)oldRootFile->Get("PHOSTriggerQAResultsL1Medium");
    histTrigL1H = (TList*)oldRootFile->Get("PHOSTriggerQAResultsL1High");
    if (histAnyInt == 0 || histPHI7 == 0) {
        printf(" does not contain PHOSCellQA histograms\n");
        continue;
    }
    else {
        printf(" contains PHOSCellQA histograms\n");
    }

    // char *runNum = strtok(rootFileName + 35, "/");

    // newRootFileName = Form("AnyInt_%s.root", runNum);
    // newRootFile = TFile::Open(newRootFileName, "recreate");
    // histAnyInt->Write(0, 0);
    // newRootFile->Close();

    // newRootFileName = Form("PHI7_%s.root", runNum);
    // newRootFile = TFile::Open(newRootFileName, "recreate");
    // histPHI7->Write(0, 0);
    // newRootFile->Close();

    // if (histTrigL0 || histTrigL1L || histTrigL1M || histTrigL1H) {
    //     newRootFileName = Form("TriggerQA_%s.root", runNum);
    //     newRootFile = TFile::Open(newRootFileName, "recreate");
    //     if (histTrigL0) histTrigL0->Write(histTrigL0->GetName(), TObject::kSingleKey);
    //     if (histTrigL1L) histTrigL1L->Write(histTrigL1L->GetName(), TObject::kSingleKey);
    //     if (histTrigL1M) histTrigL1M->Write(histTrigL1M->GetName(), TObject::kSingleKey);
    //     if (histTrigL1H) histTrigL1H->Write(histTrigL1H->GetName(), TObject::kSingleKey);
    //     newRootFile->Close();
    //     histTrigL0 ->Clear();
    //     histTrigL1L ->Clear();
    //     histTrigL1M ->Clear();
    //     histTrigL1H ->Clear();
    // }

    // histAnyInt->Clear();
    // histPHI7->Clear();

    oldRootFile->Close();
}

void merge(const TString  dirname)
{
    TList * files = TSystemDirectory(dirname, dirname).GetListOfFiles();
    for (Int_t i = 0; i < files->GetEntries(); ++i)
    {
        TSystemFile * file = (TSystemFile *) files->At(i);
        ProcessRun(file);
    }
}
