
function download_from_grid()
{
    counter=1
	MHOME=$1/
    TRAIN=$3
    for run in $(alien_ls $MHOME/); do
    	filepath=$MHOME/$run/$TRAIN/CaloCellsQA.root
    	output=$(alien_ls "$filepath") 
        if [ "$output" == "CaloCellsQA.root" ]; then
        	echo "Downloading run " $run
	        alien_cp alien://$filepath $2/$((counter++)).$run.root
        fi
        # echo $run
    done
}

download_from_grid $1 $2 $3