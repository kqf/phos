function download_from_grid()
{
    counter=1
    for run in $(alien_ls $1/); do
        # echo $run
    	filepath=$1/$run/$2/$3
    	output=$(alien_ls "$filepath") 
        # echo $output
        if [ "$output" == "$3" ]; then
        	echo "Downloading run " $run
	        alien_cp alien://$filepath $4/$((counter++)).$run.root
        fi
        # echo $run
        # until alien_cp alien://$1/$1/output/$run/$4 $2/$((counter++)).$run.root; do echo 'Trying again in 10 sec.'; sleep 10; done
    done
}

function main()
{
    # TRAIN=/pass1/PWGGA/GA_pp_AOD/354_20180320-1238_child_
    # DATAPATH=/alice/data/2017

    # TRAIN_CHILD=11
    # PERIOD=LHC17r

    # NAME=iteration1
    # # FILE_NAME=TriggerQA.root
    # DIRECTORY=$1/$PERIOD/$NAME


    TRAIN=/pass1/QA/
    DATAPATH=/alice/data/2017

    TRAIN_CHILD=""
    PERIOD=LHC17c

    NAME=default
    FILE_NAME=QAresults.root

    train_children=("" "")
    periods=("LHC17c" "LHC17e")


    for i in "${!train_children[@]}"; do 
        child=${train_children[$i]}
        period=${periods[$i]}
        directory=$1/$period/$NAME
        echo "*******************************"
        echo ""
        echo "Processing the period $period" 
        echo ""
        echo "*******************************"

        mkdir -p $directory
        download_from_grid $DATAPATH/$period $TRAIN$train_child $FILE_NAME $directory 
        hadd $directory/$period.root $directory/*.root
        find $directory -type f -not -name "$period.root" -print0 | xargs -0 rm --
    done
}


main $1
