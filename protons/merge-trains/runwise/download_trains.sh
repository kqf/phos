# Index corresponds 

declare -a periods=("LHC17c" "LHC17e" "LHC17f" "LHC17g" "LHC17i" "LHC17j" "LHC17k" "LHC17l" "LHC17m" "LHC17o")
nperiods=${#periods[@]}

echo $nperiods

function download_from_grid()
{
    counter=1
	MHOME=/alice/data/2017/$1/
	TRAIN=/pass1/PWGGA/GA_pp_AOD/334_20180217-1427_child_$3/
    for run in $(alien_ls $MHOME/); do
    	filepath=$MHOME/$run/$TRAIN/AnalysisResults.root
    	output=$(alien_ls "$filepath") 
        if [ "$output" == "AnalysisResults.root" ]; then
        	echo "Downloading run " $run
	        alien_cp alien://$filepath $2/$((counter++)).$run.root
        fi
        # echo $run
        # until alien_cp alien://$MHOME/$1/output/$run/$2 $3/$((counter++)).$run.root; do echo 'Trying again in 10 sec.'; sleep 10; done
    done
}

function main() {
    for (( i=4; i<${nperiods}+1; i++ ));
    do
        echo "Processing: " $i "/" ${nperiods} " : " ${periods[$i-1]}
        mkdir -p ${periods[$i-1]}
        download_from_grid ${periods[$i-1]} ${periods[$i-1]} $i
        hadd ${periods[$i-1]}.root ${periods[$i-1]}/*.root
    done
}

main && echo -e "\a"


# download_from_grid $1 $2 $3


