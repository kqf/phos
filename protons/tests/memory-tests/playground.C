#include <TList.h>
#include <TH1F.h>
#include <TString.h>

void playground()
{
	TH1::AddDirectory(kFALSE);
	TList list;
	list.SetOwner(kTRUE);
	for(int i; i < 100; ++i)
	{
	    TH1F * hist = new TH1F(TString("hist") + i, "Func", 100, 0, 100);
	    for(int i; i < 10000; ++i)
		    hist->Fill(i % 100, i);
		// list->Add(hist);
	}	
	list.Clear();
}
