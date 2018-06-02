outdir=results/mc/pythia/multiple_years/
ofile=pythia8.root
function upload() {
	hadd $ofile child*.root
	alien_mkdir -p $ALIEN_HOME/$outdir/
	alien_cp -n $ofile alien:$ALIEN_HOME/$outdir/$ofile@ALICE::GSI::SE2

	for i in child*.root; do
		alien_cp -n $i alien:$ALIEN_HOME/$outdir/$i@ALICE::GSI::SE2
	done
}

upload