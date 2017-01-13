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

	// First, create canvas and draw original map of bad channels
	TCanvas * canvas = DrawPHOSOBadMap("testmap", excells, nexc);

	// Second (optional), Exclude suspicious FEE(s).
	ExcludeRegion(canvas, 0, 16,  42, 44, 3);


	// Third (optional), Excludes list(s) of suspicious cells in module(s).
	//
	// Important: Due to CINT limitations one should use POINTERS here!
	//

	Cell * cells[] = { 
		new Cell(1, 43), new Cell(1, 44), new Cell(2, 43), new Cell(2, 44), new Cell(3, 43), new Cell(3, 44), new Cell(4, 43), new Cell(4, 44), new Cell(5, 43), new Cell(5, 44), 
		new Cell(6, 43), new Cell(6, 44), new Cell(7, 43), new Cell(7, 44), new Cell(8, 43), new Cell(8, 44), new Cell(9, 43), new Cell(9, 44), new Cell(10, 43), new Cell(10, 44),
		new Cell(11, 43), new Cell(11, 44), new Cell(12, 43), new Cell(12, 44), new Cell(13, 43), new Cell(13, 44), new Cell(14, 43), new Cell(14, 44), new Cell(15, 43),
		new Cell(15, 44), new Cell(16, 43), new Cell(16, 44)
	};
	Int_t ncells = sizeof(cells)/sizeof(Cell *);
	ExcludeCells(canvas, cells, ncells, 3);


	// Fourth, draw and save to a testbmap.png.
	// This name is important!
	canvas->Update();
	canvas->SaveAs("testbmap.png");

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
}

// Warning: RelPosToAbsId will not work here: It doesn't take into account misalignment.
//  		Use for loop instead.
void ExcludeCells(TCanvas * c1, Cell ** cells, Int_t ncells, Int_t inmodule)
{
	TH2 * hSM = c1->FindObject(Form("PHOS_BadMap_mod%i", inmodule));

	cout << "Cell ids from your list of bad cells" << endl;

	for (int k = (3584 * (inmodule - 1) + 1); k <= (3584 * (inmodule)  ); ++k)
	{
		Int_t nModule, xCell, zCell;
		AbsId2EtaPhi(k, nModule, xCell, zCell);
		Cell kcell(xCell, zCell);
		
		Bool_t isBadCell = kFALSE;
		for(Int_t i = 0; (i < ncells) && (!isBadCell); ++i)
			isBadCell = (( *cells[i]) ==  kcell);

		if (!isBadCell) 
			continue;

		hSM->Fill(cells[i]->first, cells[i]->second);
		cout << k << ", ";
	}	
	cout << endl;
}


