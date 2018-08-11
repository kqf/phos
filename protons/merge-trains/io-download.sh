# train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_AOD/
train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_MC_AOD/
# run=326_20180209-1536_child_
# run=334_20180217-1427_child_
# run=345_20180305-1550_child_
# run=831_20180530-1028_child_
# run=861_20180608-1521_child_
run=963_20180809-1020_child_
runlist=merge_runlist_1
# outdir=results/data/LHC17/iteration0


function download_file() {
	alien_cp alien:/$1/AnalysisResults.root $2
}

function show_dir() {
	alien_ls $1
}

function download() {
	# NB: Always check runlists awailable for merge
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

download