function download_from_grid()
{
	counter=1
	for f in $(alien_find $1 CaloCellsQA2.root | grep -i alice) 
	do 
		echo $f
		alien_cp alien://$f $2/$((counter++)).root
	done
}

download_from_grid $1 $2
