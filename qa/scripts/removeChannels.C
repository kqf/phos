#include <pair>
#include <vector>

typedef std::pair<Int_t, Int_t> Cell;
typedef std::vector<Cell> Cells;
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
	// ExcludeRegion(canvas,  0, 16, 46, 48, 2);
	// ExcludeRegion(canvas, 48, 64, 28, 30, 3);
	// ExcludeRegion(canvas, 48, 64, 46, 48, 4);


	// Third (optional), Exclude some cells.
	// Here all bins start from 1 this means that:
	// Put here x + 1, z + 1 where x, z are taken from grid.
	Cells sm1;
	{
		sm1.push_back(Cell(37, 13));
		ExcludeCells(canvas, sm1, 1);
	}

	Cells sm2;
	{
		sm2.push_back(Cell(49, 38));
		sm2.push_back(Cell(64, 47));
		sm2.push_back(Cell(63, 47));
		ExcludeCells(canvas, sm2, 2);
	}

	Cells sm3;
	{
		sm3.push_back(Cell(6, 54));
		sm3.push_back(Cell(39, 2));
		ExcludeCells(canvas, sm3, 3);
	}

	Cells sm4;
	{
		sm4.push_back(Cell(34,  2));
		ExcludeCells(canvas, sm4, 4);
	}


	// Forth, draw and save to a testbmap.png.
	// This name is important!
	canvas->Update();
	canvas->SaveAs("testbmap.png");

	// Fifth, write root file of a new badmap
	TFile ofile("testbmap.root", "recreate");
	canvas->Write();
	ofile.Close();
}

void ExcludeRegion(TCanvas * c1, Int_t startx, Int_t stopx, Int_t starty, Int_t stopy, Int_t inmodule)
{
	TH2 * hSM = c1->FindObject(Form("PHOS_BadMap_mod%i", inmodule));

	std::vector<Int_t> bad_cells;
	for (Int_t k = (3584 * (inmodule - 1) + 1); k <= (3584 * (inmodule)  ); ++k)
	{
		Int_t nModule, xCell, zCell;
		AbsId2EtaPhi(k, nModule, xCell, zCell);

		Bool_t xrange = (xCell > startx) && (xCell <= stopx);
		Bool_t zrange = (zCell > starty) && (zCell <= stopy);

		if (xrange && zrange)
		{
			hSM->Fill(xCell, zCell);
			bad_cells.push_back(k);
		}
	}

	for(Int_t i = 0; i < bad_cells.size(); ++i)
			cout << bad_cells[i] << ", ";
	cout << "// " << bad_cells.size() << " cells in sm " << inmodule << endl;
}

// Warning: RelPosToAbsId will not work here: It doesn't take into account misalignment.
//  		Use for loop instead.
void ExcludeCells(TCanvas * c1, Cells cells, Int_t inmodule)
{
	TH2 * hSM = c1->FindObject(Form("PHOS_BadMap_mod%i", inmodule));

	std::vector<Int_t> bad_cells;
	for (Int_t k = (3584 * (inmodule - 1) + 1); k <= (3584 * (inmodule)  ); ++k)
	{

		Int_t nModule, xCell, zCell;
		AbsId2EtaPhi(k, nModule, xCell, zCell);
		Cell kcell(xCell, zCell);

		Bool_t isBadCell = kFALSE;
		for (Int_t i = 0; (i < cells.size()) && (!isBadCell); ++i)
			isBadCell = (cells[i] == kcell);

		if (!isBadCell)
			continue;

		hSM->Fill(cells[i].first, cells[i].second);
		bad_cells.push_back(k);
	}

	for(Int_t i = 0; i < bad_cells.size(); ++i)
			cout << bad_cells[i] << ", ";
	cout << "// " << bad_cells.size() << " cells in sm " << inmodule << endl;
}


