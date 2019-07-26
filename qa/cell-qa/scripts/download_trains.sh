
function download_from_grid()
{
	mhome=$1
    odir=$2
    train=$3

    echo "Downloading the data from grid: $mhome $odir $train"

    counter=1
    for run in $(alien_ls $mhome/); do
    	filepath=$mhome/$run/$train/CaloCellsQA.root
        echo "Downloading from:"
        echo $filepath
    	output=$(alien_ls "$filepath") 
        if [ "$output" == "CaloCellsQA.root" ]; then
        	echo "Downloading run " $run
	        alien_cp alien://$filepath $odir/$((counter++)).$run.root
        fi
        # echo $run
    done
}

download_from_grid $1 $2 $3
