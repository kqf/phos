train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_AOD/
run=326_20180209-1536_child_
runlist=merge_runlist_3
outdir=results/data/corrected/



function download_file() {
	alien_cp alien://$1/AnalysisResults.root $2
}

function show_dir() {
	alien_ls $1
}


function download() {
	for i in {1..10}; do
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

upload