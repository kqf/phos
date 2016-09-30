function download_from_grid()
{
	counter=1
    MHOME=/alice/cern.ch/user/o/okovalen
	for f in $(alien_find $MHOME/$1 $2 | grep -i alice) 
	do 
		echo $f
		alien_cp alien://$f $3/$((counter++)).root
	done
}

download_from_grid $1 $2 $3
