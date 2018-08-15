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
	// ExcludeRegion(canvas, 32, 48, 20, 22, 4);


	// Third (optional), Exclude some cells.
	// Here all bins start from 1 this means that:
	// Put here x + 1, z + 1 where x, z are taken from grid.
	Cells sm1;
	{
		sm1.push_back(Cell(2, 30));
		sm1.push_back(Cell(2, 31));
		sm1.push_back(Cell(2, 34));
		sm1.push_back(Cell(2, 35));
		sm1.push_back(Cell(2, 36));
		sm1.push_back(Cell(2, 37));
		sm1.push_back(Cell(2, 38));
		sm1.push_back(Cell(2, 39));
		sm1.push_back(Cell(2, 40));
		sm1.push_back(Cell(2, 45));
		sm1.push_back(Cell(2, 46));
		sm1.push_back(Cell(4, 37));
		sm1.push_back(Cell(4, 38));
		sm1.push_back(Cell(4, 39));
		sm1.push_back(Cell(6, 41));
		sm1.push_back(Cell(17, 24));
		sm1.push_back(Cell(21, 9));
		sm1.push_back(Cell(21, 22));
		sm1.push_back(Cell(22, 9));
		sm1.push_back(Cell(22, 10));
		sm1.push_back(Cell(33, 50));
		sm1.push_back(Cell(34, 43));
		sm1.push_back(Cell(37, 42));
		sm1.push_back(Cell(37, 43));
		sm1.push_back(Cell(38, 42));
		sm1.push_back(Cell(38, 53));
		sm1.push_back(Cell(39, 2));
		sm1.push_back(Cell(49, 4));
		sm1.push_back(Cell(49, 7));
		sm1.push_back(Cell(49, 9));
		sm1.push_back(Cell(49, 12));
		sm1.push_back(Cell(49, 15));
		sm1.push_back(Cell(50, 4));
		sm1.push_back(Cell(50, 54));
		sm1.push_back(Cell(53, 6));
		sm1.push_back(Cell(53, 46));
		sm1.push_back(Cell(53, 47));
		sm1.push_back(Cell(53, 48));
		sm1.push_back(Cell(54, 9));
		sm1.push_back(Cell(54, 14));
		sm1.push_back(Cell(54, 45));
		ExcludeCells(canvas, sm1, 1);
	}

	Cells sm2;
	{
		sm2.push_back(Cell(2, 4));
		sm2.push_back(Cell(2, 5));
		sm2.push_back(Cell(2, 7));
		sm2.push_back(Cell(2, 9));
		sm2.push_back(Cell(2, 15));
		sm2.push_back(Cell(2, 18));
		sm2.push_back(Cell(2, 19));
		sm2.push_back(Cell(2, 21));
		sm2.push_back(Cell(2, 23));
		sm2.push_back(Cell(2, 24));
		sm2.push_back(Cell(2, 25));
		sm2.push_back(Cell(2, 28));
		sm2.push_back(Cell(2, 34));
		sm2.push_back(Cell(2, 35));
		sm2.push_back(Cell(2, 36));
		sm2.push_back(Cell(2, 37));
		sm2.push_back(Cell(2, 38));
		sm2.push_back(Cell(2, 40));
		sm2.push_back(Cell(2, 42));
		sm2.push_back(Cell(2, 54));
		sm2.push_back(Cell(2, 55));
		sm2.push_back(Cell(20, 39));
		sm2.push_back(Cell(22, 2));
		sm2.push_back(Cell(28, 53));
		sm2.push_back(Cell(29, 53));
		sm2.push_back(Cell(30, 53));
		sm2.push_back(Cell(33, 53));
		sm2.push_back(Cell(33, 55));
		sm2.push_back(Cell(34, 5));
		sm2.push_back(Cell(34, 55));
		sm2.push_back(Cell(37, 4));
		sm2.push_back(Cell(37, 5));
		sm2.push_back(Cell(38, 5));
		sm2.push_back(Cell(49, 13));
		sm2.push_back(Cell(49, 23));
		sm2.push_back(Cell(49, 31));
		sm2.push_back(Cell(49, 33));
		sm2.push_back(Cell(53, 39));
		ExcludeCells(canvas, sm2, 2);
	}

	Cells sm3;
	{
		sm3.push_back(Cell(2, 4));
		sm3.push_back(Cell(2, 6));
		sm3.push_back(Cell(2, 24));
		sm3.push_back(Cell(2, 25));
		sm3.push_back(Cell(2, 26));
		sm3.push_back(Cell(2, 27));
		sm3.push_back(Cell(2, 29));
		sm3.push_back(Cell(2, 31));
		sm3.push_back(Cell(2, 33));
		sm3.push_back(Cell(2, 35));
		sm3.push_back(Cell(2, 36));
		sm3.push_back(Cell(2, 48));
		sm3.push_back(Cell(2, 49));
		sm3.push_back(Cell(2, 50));
		sm3.push_back(Cell(18, 38));
		sm3.push_back(Cell(18, 40));
		sm3.push_back(Cell(18, 42));
		sm3.push_back(Cell(32, 10));
		sm3.push_back(Cell(49, 3));
		sm3.push_back(Cell(50, 2));
		sm3.push_back(Cell(51, 2));
		ExcludeCells(canvas, sm3, 3);
	}

	Cells sm4;
	{
		sm4.push_back(Cell(33, 2));
		sm4.push_back(Cell(34, 9));
		sm4.push_back(Cell(34, 14));
		sm4.push_back(Cell(34, 48));
		sm4.push_back(Cell(36, 47));
		sm4.push_back(Cell(37, 47));
		sm4.push_back(Cell(49, 5));
		sm4.push_back(Cell(49, 54));
		sm4.push_back(Cell(49, 55));
		sm4.push_back(Cell(50, 55));
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


