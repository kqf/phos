outdir=results/data/LHC17/qa1
ofile=LHC17.root
# outdir=results/mc/pythia/ep_ratio_1
# ofile=pythia8.root
function upload() {
	hadd $ofile *.root
	alien_mkdir -p $ALIEN_HOME/$outdir/
	alien_cp -n $ofile alien:$ALIEN_HOME/$outdir/$ofile@ALICE::GSI::SE2

	for i in *.root; do
		alien_cp -n $i alien:$ALIEN_HOME/$outdir/$i@ALICE::GSI::SE2
	done
}

upload