function download_from_grid()
{
	counter=1
    MHOME=/alice/cern.ch/user/o/okovalen
	for run in $(alien_find $MHOME/$1/output/$2/ $3 | grep .root); do echo $run; alien_cp alien:$run tmp_results/$((counter++)).root; done
}

# download_from_grid Task SEED filename
download_from_grid $1 $2 $3