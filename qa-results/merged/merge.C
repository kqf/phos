void merge(TString directory = "..", TString oname = "CaloCellsQA", TString cname = "PHOSCellsQA") 
{
	TH1::AddDirectory(kFALSE);
	TList * files = TSystemDirectory(directory, directory).GetListOfFiles();
	if (!files) return;

	TList * output = new TList();
	output->SetOwner(kTRUE);

	for(Int_t i = 0; i < files->GetEntries(); ++i)
	{
		TSystemFile * file = dynamic_cast<TSystemFile *>(files->At(i));
		TString fname = file->GetName();
		if (file->IsDirectory() || !fname.EndsWith(".root")) continue;

		fname = directory + "/" + fname;
		cout << fname << endl;
		merge_file(fname, output, oname.Contains("TriggerQA"));
	}

    TFile fout2(directory + "/" + oname + "Single.root", "recreate");
    output->Write(cname, TObject::kSingleKey);
    fout2.cd();
    fout2.Write();
    fout2.Close();

    TFile fout1(directory + "/" + oname + ".root", "recreate");
    fout1.cd();
    output->Write();
    fout1.Write();
    fout1.Close();
}

void merge_file(const char * filename, TList * output, Bool_t add_lists)
{
	gROOT->Clear();
	if(!output) return;


	TFile file(filename, "read");
	TList * input = dynamic_cast<TList *>(get_container(file));

	if(!input)
	{
		cout << "Container is not a list!!!" << endl;
		return;
	}

	add_list(output, input, add_lists);
	file.Close();
}

void add_list(TList * output, TList * input, Bool_t add_lists)
{


	TList * previous = dynamic_cast<TList *>(output->FindObject(input->GetName()));
	if(!previous && add_lists)
	{
		output->Add(input->Clone());
		delete input;
		return;
	}

	TList * to_merge = add_lists ? previous : output; // Decide wheter to add to output list or to sublist in output list


	for(Int_t i = 0; i < input->GetEntries(); ++i)
	{
		TObject * entry = input->At(i);
		add_object(to_merge, entry);
	}
	if(input) delete input;
}

void add_object(TList * output, TObject * entry)
{
	TH1 * hist = dynamic_cast<TH1 *>(entry);
	if(hist)
	{
		TH1 * hist_old = dynamic_cast<TH1*>(output->FindObject(hist->GetName()));
		if(hist_old)
			hist_old->Add(hist);
		else
			output->Add(hist->Clone(hist->GetName()));
		return;
	}	

	TList * inlist = dynamic_cast<TList * >(entry);
	if(inlist)
	{
		cout << inlist->GetName() << endl;
		add_list(output, inlist);
		return;
	}


	cout << "Warning: You are trying to add neither TList nor TH1 histogram! Check/Upate your code." << endl;
}

TObject * get_container(TFile & file)
{
	const Int_t nposs_containers = 4;
	const char * names[nposs_containers] = {"PHOSCellsQA2", "PHOSCellsQA1", "PHOSCellsQA", "TriggerQA" } ;
	for(Int_t i = 0; i < nposs_containers; ++i)
	{
		TObject * result  = file.Get(names[i]);
		if(result) return result;
	}
	cout << "Warning: you might want to add your container to the list of possible containers" << endl;
	file.ls();
	return 0;
}