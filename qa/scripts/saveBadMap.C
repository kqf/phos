void saveBadMap(const char * period = "", TString filename = "")
{
	// If no geometry class -- nothing to do here
	if (!gROOT->GetClass("AliPHOSGeometry"))
		return;
	SetupGeometry();

	gROOT->SetBatch();
	// gStyle->SetOptStat(0);

	gROOT->LoadMacro("../../protons/datasets/values_for_dataset.h+");

	std::vector<Int_t> v;
	values_for_dataset(v, TString(period).Contains("16") ? "BadCells_LHC16" : "", "../../protons/datasets/");

	Int_t nexc = v.size();
	Int_t * excells = new Int_t[nexc];

	for (Int_t i = 0; i < nexc; ++i)
		excells[i] = v[i];


	if (filename.Length())
	{
		// Just read a file if file name is specified
		// othervise extract Bad channel map
		cout << "Here " << bool(filename) << endl;
		ReadPrintBadCells(period, excells, nexc, filename);
		return;
	}

	DrawPHOSOBadMap(period, excells, nexc);


	cout << "# excluded cells for this badmap " << nexc << endl;
	// Verify the BadMap
	ReadPrintBadCells(period, excells, nexc);
}

//_________________________________________________________________________
TCanvas * DrawPHOSOBadMap(char * cname = "LHC16g", Int_t * excells = 0, Int_t nexc)
{
	// Draw bad cell map for PHOS;
	// cname -- canvas name.

	const Int_t nmods = 4; // number of supermodules
	TCanvas * c1 = new TCanvas(cname, cname, 4 * 64 * 10, 4 * 56 * 10);
	c1->Divide(nmods / 2, 2);

	TFile * fBadMap = TFile::Open(Form("BadMap_%s.root", cname), "recreate");
	for (Int_t sm = 1; sm <= nmods; sm++)
	{
		c1->cd(sm);
		gPad->SetLeftMargin(0.10);
		gPad->SetRightMargin(0.15);
		gPad->SetTopMargin(0.05);
		gPad->SetBottomMargin(0.10);

		TH2 * hSM = InitiateHistogramForSM(sm, excells, nexc);
		hSM->Write();
		hSM->DrawCopy("colz");
	}

	fBadMap->Close();
	c1->Update();
	c1->SaveAs(TString("BadMap_") + TString(c1->GetName()) + ".pdf");
	return c1;
}

TH2 * InitiateHistogramForSM(Int_t sm, Int_t * excells, Int_t nexc)
{
	TH2 * hSM = new TH2F(Form("PHOS_BadMap_mod%i", sm), Form("Bad Channel Map in Module %i", sm), 64, 0.5, 64.5, 56, 0.5, 56.5);
	for (Int_t i = 0; i < nexc; ++i)
	{
		bool lower_cut = excells[i] >= (3584 * (sm - 1) + 1);
		bool upper_cut = excells[i] <= (3584 * (sm)  );

		if ( !(lower_cut && upper_cut) ) continue;
		Int_t nModule, xCell, zCell;
		AbsId2EtaPhi(excells[i], nModule, xCell, zCell);
		hSM->Fill(xCell, zCell);
	}
	return hSM;
}

void ReadPrintBadCells(char * cname = "LHC16g", Int_t * ref = 0, int nexc = 0, TString filepath = "")
{
	// Draw bad cell map for PHOS;

	TString fname = filepath.Length() ? filepath : Form("BadMap_%s.root", cname);
	TFile * bfile = TFile::Open(fname);

	gROOT->cd();

	TH2 * badmap[4] = {0};
	for (Int_t module = 1; module <=  4; ++module)
	{
		TH2I * h = (TH2I *) bfile->Get(Form("PHOS_BadMap_mod%d", module));
		badmap[module - 1] = new TH2I(*h);
		cout << "Set " <<  badmap[module - 1]->GetName() << endl;
	}

	bfile->Close();
	cout << "\n\n...PHOS BadMap is set now." << endl;

	std::vector<int> excells;
	// Reading the cells
	for (Int_t sm = 1; sm <= 4; sm++)
	{
		int start = (3584 * (sm - 1) + 1);
		int stop  = (3584 * (sm) + 1);
		for (Int_t i = start; i < stop; ++i) // loop over cell absolute ids
		{
			Int_t nModule, xCell, zCell;
			AbsId2EtaPhi(i, nModule, xCell, zCell);

			if ( badmap[sm - 1]->GetBinContent(xCell, zCell) > 0)
				excells.push_back(i);
		}
	} // supermodule loop

	cout << "Int_t excells[] = {";
	for (int i = 0; i < excells.size(); ++i)
	{
		char * suff = (i == (excells.size() - 1)) ? "" : ",";
		cout << excells[i] << suff;
	}
	cout << "};\n";
	cout << "Int_t nexc = " << excells.size() << ";"  << endl;

	Int_t nModule, xCell, zCell;
	AbsId2EtaPhi(3585, nModule, xCell, zCell);

	for (int i = 0; i < nexc; ++i)
	{
		if (ref[i] == excells[i]) continue;
		cout << "ERROR: found deviation in how I read and write the Bad Map" << excells[i] << endl;
		break;
	}


}

void AbsId2EtaPhi(Int_t absId, Int_t & nModule, Int_t & phi, Int_t & eta)
{
	// Converts cell absId --> (sm,eta,phi);
	AliPHOSGeometry * geomPHOS = AliPHOSGeometry::GetInstance("Run2");

	Int_t relid[4];
	geomPHOS->AbsToRelNumbering(absId, relid);
	//sm = relid[0];

	phi = relid[2];
	eta = relid[3];
}


void SetupGeometry()
{
	AliPHOSGeometry * geo = AliPHOSGeometry::GetInstance("Run2");

	AliOADBContainer geomContainer("phosGeo");
	geomContainer.InitFromFile("$ALICE_PHYSICS/OADB/PHOS/PHOSGeometry.root", "PHOSRotationMatrixes");
	TObjArray * matrixes = (TObjArray *)geomContainer.GetObject(258391, "PHOSRotationMatrixes");

	for (Int_t mod = 0; mod < 5; mod++)
	{
		if (!matrixes->At(mod)) continue;
		geo->SetMisalMatrix(((TGeoHMatrix *)matrixes->At(mod)), mod) ;
		cout << (Form("Adding PHOS Matrix for mod:%d, geo=%p\n", mod, geo)) << endl;
	}
}
