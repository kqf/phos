
function download_from_grid()
{
    counter=1
	MHOME=/alice/data/2017/$1/
    TRAIN=/pass1/PWGGA/GA_pp_AOD/$3
    for run in $(alien_ls $MHOME/); do
    	filepath=$MHOME/$run/$TRAIN/CaloCellsQA.root
    	output=$(alien_ls "$filepath") 
        if [ "$output" == "CaloCellsQA.root" ]; then
        	echo "Downloading run " $run
	        alien_cp alien://$filepath $2/$((counter++)).$run.root
        fi
        # echo $run
        # until alien_cp alien://$MHOME/$1/output/$run/$2 $3/$((counter++)).$run.root; do echo 'Trying again in 10 sec.'; sleep 10; done
    done
}

download_from_grid $1 $2 $3