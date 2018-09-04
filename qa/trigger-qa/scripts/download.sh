TARGET=TriggerQA.root

function download_file() {
    alien_cp alien:/$1/$TARGET $2
}

function show_dir() {
    alien_ls $1
}

function main() {
    # MC trains here
    # Data trains here
    train=/alice/cern.ch/user/a/alitrain/PWGGA/GA_pp_AOD/
    run=448_20180830-1147_child_
    # This scheme is valid for LHC16 data.
    # fill the map in the following way ([child number]=runlist number)
    declare -A children=([2]=3 [3]=3 [4]=3 [5]=3 [6]=4 [7]=3 [8]=3 [9]=3)
    declare -A names=([2]=LHC16g [3]=LHC16h [4]=LHC16i [5]=LHC16j [6]=LHC16k [7]=LHC16l [8]=LHC16o [9]=LHC16p)

    # NB: Always check runlists awailable for merge
    for i in ${!children[@]}; do
        runlist=merge_runlist_${children[$i]}
        outdir=$1/${names[$i]}

        # Create
        mkdir -p $outdir
        oname=$outdir/${names[$i]}.root
        echo $train$run$i/$runlist
        {
            download_file $train$run$i/$runlist $oname 
        } || {
            download_file $train$run$i/merge $oname 
        }
    done
}

main $1