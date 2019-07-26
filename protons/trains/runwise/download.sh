# Index corresponds to each period
YEAR=2018
MAINDIR=
# TRAIN=696_20190205-1725
# TRAIN=728_20190227-1303 
# TRAIN=736_20190307-1551
TRAIN=908_20190724-1352 
TRAIN_PATH=pass1/AOD208/PWGGA/GA_pp_AOD/${TRAIN}_child_
TARGET_FILE=CaloCellsQA.root

declare -A children=([1]=5 [2]=5 [3]=5 [4]=5 [5]=5 [6]=5 [7]=5 [8]=5 [9]=5 [10]=5 [11]=5 [12]=5 [13]=5, [14]=5)
declare -A names=([1]=LHC18b [2]=LHC18d [3]=LHC18e [4]=LHC18f [5]=LHC18g [6]=LHC18h [7]=LHC18i [8]=LHC18j [9]=LHC18k [10]=LHC18l [11]=LHC18m [12]=LHC18n [13]=LHC18o [14]=LHC18p)

function download_from_grid()
{
    period=$1
    child=$2

    workdir=/alice/data/${YEAR}/${period}/
    echo ${workdir}
    for run in $(alien_ls ${workdir}/); do
    	filepath=${workdir}/${run}/${TRAIN_PATH}${child}/${TARGET_FILE}
    	output=$(alien_ls "${filepath}") 
        echo $output
        if [ "${output}" == "${TARGET_FILE}" ]; then
        	echo "Downloading run " ${run}
	        alien_cp alien://${filepath} ${period}/${run}.root
            echo alien://${filepath} ${period}/${run}.root
        fi
    done
}

function main() {
    for child in ${!children[@]}; do
        period=${names[$child]}
        echo "Processing: " ${period}
        mkdir -p ${period}
        # download_from_grid ${period} $child
        root -l -b -q merge.C"(\"${period}\")"
    done
}

main && echo -e "\a"

# download_from_grid $1 $2 $3
