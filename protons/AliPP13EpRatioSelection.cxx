//________________________________________________________________
void AliPP13EpRatioSelection::InitSelectionHistograms()
{
	// pi0 mass spectrum
	Int_t nM       = 50;
	Double_t mMin  = 0.0;
	Double_t mMax  = 2.;
	Int_t nPt      = 400;
	Double_t ptMin = 0;
	Double_t ptMax = 20;

	for (Int_t i = 0; i < 2; ++i)
	{
		const char * species = (i == 0) ? "Electrons" : "Non-Electron";

		TH2 * patternP = new TH2F(
			Form("hEp%sP", species), 
			"E/p ratio vs. E_{cluster} M%d; E/p; E^{track} ,GeV", 
			nM, mMin, mMax, nPt, ptMin, ptMax
		);

		fEpP[i] = new AliPP13DetectorHistogram(
			patternP,
			fListOfHistos, 
			AliPP13DetectorHistogram::kModules
		);

		TH2 * patternPt = new TH2F(
			Form("hEp%sP", species), 
			"E/p ratio vs. E_{cluster} M%d; E/p; p_{T}^{track} ,GeV/c", 
			nM, mMin, mMax, nPt, ptMin, ptMax
		);

		fEpPt[i] = new AliPP13DetectorHistogram(
			patternPt,
			fListOfHistos,
			AliPP13DetectorHistogram::kModules
		);
	}

	fTPCSignal[0] = new TH2F("hEpRatioNSigmaElectron", "E/p ratio vs. N_{#sigma}^{e}; E/p; n#sigma^{e}",nM, mMin, mMax, 20, -5, 5); 
    fTPCSignal[1] = new TH2F("hTPCSignal_Electron", "TPC dE/dx vs. electron momentum; p^{track}, GeV/c; dE/dx, a.u.",40, 0, 20, 200, 0, 200); 
	fTPCSignal[2] = new TH2F("hTPCSignal_Non-Electron", "TPC dE/dx vs. non-electron momentum; p^{track}, GeV/c; dE/dx, a.u.",40, 0, 20, 200, 0, 200);
	fTPCSignal[3] = new TH2F("hTPCSignal_Non-Electron", "TPC dE/dx vs. all particles momentum; p^{track}, GeV/c; dE/dx, a.u.",40, 0, 20, 200, 0, 200);

	for (int i = 0; i < 4; ++i)
		fListOfHistos->Add(fTPCSignal[i]);

	for (Int_t i = 0; i < fListOfHistos->GetEntries(); ++i)
	{
		TH1 * hist = dynamic_cast<TH1 *>(fListOfHistos->At(i));
		if (!hist) continue;
		hist->Sumw2();
	}

	// These histograms are needed only to check the performance
	// Don't do any analysis with these histograms.
	//

	fClusters = new TH1F("hClusterPt_SM0", "Cluster p_{T} spectrum with default cuts, all modules; p_{T}, GeV/c", nPt, ptMin, ptMax);	
	fListOfHistos->Add(fClusters);
}

void AliPP13EpRatioSelection::FillClusterHistograms(const AliVCluster * cluster, const EventFlags & eflags)
{
	// No tracks
	if( !(cluster->GetNTracksMatched() > 0) )
		return;

	AliVTrack * track = dynamic_cast<AliVTrack*>(cluster->GetTrackMatched(0));

	// The track wasn't found
	if(!track)
		return;

	Bool_t isHybridTrack = dynamic_cast<AliAODTrack*>(track)->IsHybridGlobalConstrainedGlobal();//hybrid track

	// Take only hybrid tracks
	if(!isHybridTrack)
		return;

	Double_t energy = cluster->Energy();
	Double_t trackP = track->P();
	Double_t trackPt = track->Pt();
	Double_t dEdx = track->GetTPCsignal();
	Double_t EpRatio = energy / trackP;

	fTPCSignal[1]->Fill(trackP, dEdx);

	// TODO: Accept electron cuts
	// TODO: Ensure not neutra particles
	//

	Double_t nSigma = eflags.fPIDResponse->NumberOfSigmasTPC(track, AliPID::kElectron);

	fTPCSignal[0]->Fill(EpRatio, nSigma);
	Bool_t isElectron = (-2 < nSigma && nSigma < 3) ;


	if(isElectron)
	{
		fEpP[0]->Fill(EpRatio, energy);
		fEpPt[0]->Fill(EpRatio, trackPt);
		fTPCSignal[2]->Fill(trackP, dEdx);
	}
	else if(nSigma < -3 || 5 < nSigma)
	{
		fEpP[1]->Fill(EpRatio, energy);
		fEpPt[1]->Fill(EpRatio, trackPt);
		fTPCSignal[3]->Fill(trackP, dEdx);
	}
}


//________________________________________________________________
void AliPP13EpRatioSelection::FillPi0Mass(TObjArray * clusArray, TList * pool, const EventFlags & eflags)
{
	// Ensure that we are not doing mixing
	EventFlags flags = eflags;
	flags.isMixing = kFALSE;

	// Select photons
	TObjArray photonCandidates;
	SelectPhotonCandidates(clusArray, &photonCandidates, flags);
}