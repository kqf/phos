# Index corresponds to each period
MAINDIR=/alice/data/2016
TRAIN=696_20190205-1725
TRAIN_PATH=pass1/AOD208/PWGGA/GA_pp_AOD/${TRAIN}_child_

declare -A children=([4]=5 [5]=5 [6]=5 [7]=5 [8]=5 [9]=5 [10]=5 [11]=5)
declare -A names=([4]=LHC16g [5]=LHC16h [6]=LHC16i [7]=LHC16j [8]=LHC16k [9]=LHC16l [10]=LHC16o [11]=LHC16p)

function download_from_grid()
{
    outdir=$1
    workdir=${MAINDIR}/${outdir}/
    train_child=${TRAIN_PATH}$2/
    echo ${workdir}
    for run in $(alien_ls ${workdir}/); do
    	filepath=${workdir}/${run}/${train_child}/AnalysisResults.root
    	output=$(alien_ls "$filepath") 
        if [ "$output" == "AnalysisResults.root" ]; then
        	echo "Downloading run " ${run}
	        alien_cp alien://${filepath} ${outdir}/${run}.root
            # echo alien://${filepath} ${outdir}/${run}.root
        fi
    done
}

function main() {
    for child in ${!children[@]}; do
        period=${names[$child]}
        echo "Processing: " ${period}
        mkdir -p ${period}
        download_from_grid ${period} $child
        echo ${period}.root ${period}/*.root
    done
}

main && echo -e "\a"

# download_from_grid $1 $2 $3
