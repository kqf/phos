function main()
{
	outdir=$1
	for period in $(ls $outdir)
	do
		filepath=$outdir/$period/$period.root
		echo $filepath
		root -l -b -q "DrawTriggerQA.C(\"$filepath\")"
		mv *.pdf $outdir/$period
	done
}


main $1 $2