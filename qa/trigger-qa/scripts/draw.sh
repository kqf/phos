function main()
{
	outdir=$1
	iteration=$2
	for period in $(ls $outdir)
	do
		filepath=$outdir/$period/$iteration/$period.root
		echo $filepath
		root -l -b -q "DrawTriggerQA.C(\"$filepath\")"
		mv *.eps $outdir/$period/$iteration
	done
}


main $1 $2