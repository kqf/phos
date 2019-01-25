// Usage:
// The second parameter should be in the form selection/list.
// Example: "PHOSEpRatio/PHOSEpRatioCoutput1"
//

void folder2list(const char * filename, const char * path)
{
	TFile * file = new TFile(filename, "update");
	
	TList * selection = dynamic_cast<TList *>(file->Get(path));
	selection->ls();
	selection->Write(selection->GetName(), TObject::kSingleKey);

	file->Write();
	file->Close();
}
