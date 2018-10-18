# MC trains here
# train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_MC_AOD/
# run=326_20180209-1536_child_
# run=334_20180217-1427_child_
# run=345_20180305-1550_child_
# run=831_20180530-1028_child_
# run=861_20180608-1521_child_
# run=963_20180809-1020_child_
# run=971_20180815-1556_child_
# run=980_20180827-1016_child_
# run=1046_20180911-0906_child_
# Dataset: LHC17_PYT8_13TeV_anchLHC16x_AOD
# declare -A children=([1]=1 [2]=1 [3]=1 [4]=1 [5]=1 [6]=1 [7]=1 [8]=1 [9]=1 [10]=1)
# declare -A names=([1]=LHC17f6 [2]=LHC17f9 [3]=LHC17d17 [4]=LHC17f5 [5]=LHC17d3 [6]=LHC17e5 [7]=LHC17d20a1 [8]=LHC17d20a2 [9]=LHC17d16 [10]=LHC17d18)

# Data trains here
train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_AOD/
# run=444_20180827-1128_child_
run=500_20181015-1127_child_
# This scheme is valid for LHC16 data.
# fill the map in the following way ([child number]=runlist number)
declare -A children=([2]=3 [3]=3 [4]=3 [5]=3 [6]=5 [7]=3 [8]=3 [9]=3)
declare -A names=([2]=LHC16g [3]=LHC16h [4]=LHC16i [5]=LHC16j [6]=LHC16k [7]=LHC16l [8]=LHC16o [9]=LHC16p)

function download_file() {
	alien_cp alien:/$1/AnalysisResults.root $2
}

function show_dir() {
	alien_ls $1
}

function download() {
	# NB: Always check runlists awailable for merge
	for i in ${!children[@]}; do
		runlist=merge_runlist_${children[$i]}
		oname=${names[$i]}.root
		echo "_________________"
		echo "                 "
		echo $train$run$i/$runlist
		{
			download_file $train$run$i/$runlist $oname 
		} || {
			download_file $train$run$i/merge $oname 
		}
	done
}

download