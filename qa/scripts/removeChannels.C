#include <pair>
#include <vector>

typedef std::pair<Int_t, Int_t> Cell;

// This scripts removes channels manually

void removeChannels()
{
	gROOT->LoadMacro("saveBadMap.C");
	SetupGeometry();

	gROOT->SetBatch();
	gStyle->SetOptStat(0);

	Int_t * excells;
	Int_t nexc = 0;

	gROOT->LoadMacro("../qa-task/getRunsBadCells.C");
	getRunsBadCells("LHC16o", 0, 0, excells, nexc);

	TCanvas * canvas = DrawPHOSOBadMap("testmap", excells, nexc); //
	cout << std::make_pair(1, 1).first << endl;

	// Excludes suspicious FEE.
	ExcludeRegion(canvas, 0, 16,  42, 44, 3);

	// Important: Due to CINT limitations one should use POINTERS here!
	Cell * cells[] = { new Cell(0, 0), new Cell(0, 0), new Cell(12, 12)};
	Int_t ncells = sizeof(cells)/sizeof(Cell *);
	ExcludeCells(canvas, cells, ncells, 2);

}

// TODO: Rewrite this using Rel to abs id and test simple
// Example:
//			ExcludeRegion(canvas, 0, 16,  42, 44, 3); 
// 
//          Output:
//  7211, 7212, 7267, 7268, 7323, 7324, 7379, 7380, 7435, 7436, 7491, 7492, 7547, 7548, 7603, 7604, 7659, 7660, 7715, 7716, 7771, 7772, 7827, 7828, 7883, 7884, 7939, 7940, 7995, 7996, 8051, 8052, 
// 

void ExcludeRegion(TCanvas * c1, Int_t startx, Int_t stopx, Int_t starty, Int_t stopy, Int_t inmodule)
{
	TH2 * hSM = c1->FindObject(Form("PHOS_BadMap_mod%i", inmodule));

	cout << "Cell ids from your FEE card:" << endl;
	for (int k = (3584 * (inmodule - 1) + 1); k <= (3584 * (inmodule)  ); ++k)
	{
		Int_t nModule, xCell, zCell;
		AbsId2EtaPhi(k, nModule, xCell, zCell);

		Bool_t xrange = (xCell > startx) && (xCell <= stopx);
		Bool_t zrange = (zCell > starty) && (zCell <= stopy);

		if (xrange && zrange)
		{
			hSM->Fill(xCell, zCell);
			cout << k << ", ";
		}
	}
	cout << endl;
	c1->Update();
	c1->SaveAs("testbmap.png");
}

void ExcludeCells(TCanvas * c1, Cell ** cells, Int_t ncells, Int_t inmodule)
{
	TH2 * hSM = c1->FindObject(Form("PHOS_BadMap_mod%i", inmodule));

	cout << "Cell ids from your list of bad cells" << endl;
	for(Int_t i = 0; i < ncells; ++i)
	{
		hSM->Fill(cells[i]->first, cells[i]->second);

		Int_t k = 0;
		RelPosToAbsId(inmodule, cells[i]->first, cells[i]->second, k);
		cout << k << ", ";
	}
	cout << endl;
}


