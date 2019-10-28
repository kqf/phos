period=LHC17
outdir=results/data/$period/extended_pt_range_1
ofile=$period.root
# alice_site=@ALICE::GSI::SE2
# outdir=results/mc/pythia/final_nonlinearity_2
# ofile=pythia8_LHC16_extra.root

function folders2lists() {
	root -l -b -q folder2list.C"(\"$1\", \"PHOSEpRatio/PHOSEpRatioCoutput1\")"
}

function upload() {
	hadd $ofile *.root
	
	# Convert all necessary folders to lists
	folders2lists $ofile

	# Interact with GRID
	alien_mkdir -p $ALIEN_HOME/$outdir/
	alien_cp -n $ofile alien:$ALIEN_HOME/$outdir/$ofile$alice_site

	for i in *.root; do
		alien_cp -n $i alien:$ALIEN_HOME/$outdir/$i$alice_site
	done
}

upload
