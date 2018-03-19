train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_AOD/
# run=326_20180209-1536_child_
# run=334_20180217-1427_child_
run=345_20180305-1550_child_

runlist=merge_runlist_3
outdir=results/data/LHC17/iteration0



function download_file() {
	alien_cp alien://$1/AnalysisResults.root $2
}

function show_dir() {
	alien_ls $1
}


function download() {
	# NB: Always check runlists awailable for merge
	for i in {1..11}; do
		echo "_________________"
		echo "                 "
		echo $train$run$i/$runlist
		{
			download_file $train$run$i/$runlist child$i.root
		} || {
			download_file $train$run$i/merge child$i.root
		}
	done
}


function upload() {
	hadd LHC16.root child*.root
	alien_cp -n LHC16.root alien:$ALIEN_HOME/$outdir/@ALICE::GSI::SE2

	for i in child*.root; do
		alien_cp -n $i alien:$ALIEN_HOME/$outdir/@ALICE::GSI::SE2
	done
}


# show_dir
download