# outdir=results/data/LHC16/ep_ratio_4
# ofile=LHC16.root
outdir=results/mc/pythia/ep_ratio_3
ofile=pythia8_LHC17.root

function folders2lists() {
	root -l -b -q folder2list.C"(\"$1\", \"PHOSEpRatio/PHOSEpRatioCoutput1\")"
}

function upload() {
	hadd $ofile *.root
	
	# Convert all necessary folders to lists
	folders2lists $ofile

	# Interact with GRID
	alien_mkdir -p $ALIEN_HOME/$outdir/
	alien_cp -n $ofile alien:$ALIEN_HOME/$outdir/$ofile@ALICE::GSI::SE2

	for i in *.root; do
		alien_cp -n $i alien:$ALIEN_HOME/$outdir/$i@ALICE::GSI::SE2
	done
}

upload
