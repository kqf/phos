#include "AliPHOSGeometry.h"
#include "AliAnalysisTaskSE.h"

#include "AliVEvent.h"
#include "AliLog.h"
#include "TH1.h"
#include "TList.h"
#include "TString.h"

#include "iostream"

void RelativeCoordinates(Int_t absId, Int_t & sm, Int_t & cellX, Int_t & cellZ)
{
	// Converts cell absId --> (sm, cellX, cellZ);
	AliPHOSGeometry * geomPHOS = AliPHOSGeometry::GetInstance("Run2");

	Int_t relid[4];
	geomPHOS->AbsToRelNumbering(absId, relid);
	sm    = relid[0];
	cellX = relid[2];
	cellZ = relid[3];
}

class AliAnalysisTaskPHOSHeatMap : public AliAnalysisTaskSE
{
public:
	AliAnalysisTaskPHOSHeatMap(): AliAnalysisTaskSE(), fOutputContainer(0), fMaps(), fNBad(0), fBadCells(0) {}
	AliAnalysisTaskPHOSHeatMap(const char * name): AliAnalysisTaskSE(name), fOutputContainer(0), fMaps(), fNBad(0), fBadCells(0)
	{
		DefineOutput(1, TList::Class());
	}

	virtual void UserCreateOutputObjects()
	{
		fOutputContainer = new TList();
		fOutputContainer->SetOwner(kTRUE);
		for (Int_t i = 0; i < 4; ++i)
		{
			fMaps[i] = new TH2F(Form("hHeatMapInSM%d", i + 1), Form("Heat map: cells fired in selected crlusters in SM%d", i), 64, 0.5, 64.5, 56, 0.5, 56.5);
			fOutputContainer->Add(fMaps[i]);
		}
		PostData(1, fOutputContainer);
	}

	virtual void UserExec(Option_t * option)
	{
		AliVEvent * event = InputEvent();


		// Check event
		if (!event) return;


		// Initialize geometry
		if (!AliPHOSGeometry::GetInstance())
		{
			AliInfo("PHOS geometry not initialized, initializing it for you");
			AliPHOSGeometry::GetInstance("Run2");
		}

		// Primary vertex
		AliVVertex * vertex = (AliVVertex *) event->GetPrimaryVertex();
		if (!vertex)
		{
			AliWarning("Could not get primary vertex");
			return;
		}

		for (Int_t i = 0; i < event->GetNumberOfCaloClusters(); i++)
		{
			AliVCluster * cluster = event->GetCaloCluster(i);
			if (!cluster)
			{
				AliWarning("Could not get cluster");
				return;
			}

			if (!cluster->IsPHOS())
				continue;

			// Reject CPV clusters
			if (cluster->GetType() != AliVCluster::kPHOSNeutral)
				continue;

			if (IsClusterBad(cluster))
				continue;

			if (cluster->GetNCells() < 3)
				continue;

			if (cluster->E() < 0.3)
				continue;

			FillHistogramsForCluster(cluster);
		}

		PostData(1, fOutputContainer);
	}


	void FillHistogramsForCluster(AliVCluster * cluster)
	{
		for (Int_t c = 0; c < cluster->GetNCells(); ++c)
		{
			Int_t cellId, sm, cellZ, cellX;
			cellId = cluster->GetCellAbsId(c);
			RelativeCoordinates(cellId, sm, cellX, cellZ);

			if (sm > 4 || sm < 1)
			{
				AliError(Form("Wrong supermodule %d", sm));
				cout << ">> " << cellId << " " << sm << " " << cellZ << " " <<  cellX << endl;
				continue;
			}
			// cout << ">>>>>>>>" << sm << " " /* << fMaps[sm] */<< endl;
			fMaps[sm - 1]->Fill(cellX, cellZ);
		}
	}

	virtual ~AliAnalysisTaskPHOSHeatMap()
	{
		delete [] fMaps;
		delete fOutputContainer;
	}


	void SetBadCells(Int_t badcells[], Int_t nbad)
	{
		if (fBadCells) delete [] fBadCells;

		if (nbad <= 0)
		{
			fNBad = 0;
			return;
		}

		fNBad = nbad;
		fBadCells = new Int_t[nbad];

		for (Int_t i = 0; i < nbad; i++)
			fBadCells[i] = badcells[i];
	}

private:
	Bool_t IsClusterBad(AliVCluster * clus)
	{
		// Returns true if cluster contains a bad cell

		for (Int_t b = 0; b < fNBad; b++)
			for (Int_t c = 0; c < clus->GetNCells(); c++)
				if (clus->GetCellAbsId(c) == fBadCells[b])
					return kTRUE;

		return kFALSE;
	}

	TList * fOutputContainer; //!
	TH2F * fMaps[4]; //!

	Int_t            fNBad;    // number of entries in fBadCells
	Int_t      *     fBadCells;//[fNBad] bad cells array


	ClassDef(AliAnalysisTaskPHOSHeatMap, 1);
};
