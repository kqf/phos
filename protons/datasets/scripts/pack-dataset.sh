archive="MC13TeV.tar.gz"
# pattern="LHC17?-pass1.txt"
prefix="verified-"


function main(){
	# Clean the directory
	rm $prefix*

	# Add comas at the end of each file
	for file in LHC18c13 LHC18c12 LHC17i4_2 LHC18a9 LHC18a8 LHC17l5 LHC17k4 LHC17h11; do
		echo $file
		sed '$!s/$/,/' $file.txt > tmp-$prefix$file
		(tr -d '\n' < tmp-$prefix$file)>>$prefix$file.txt
		rm tmp-$prefix$file
	done

	tar czvf $archive $prefix*
	rm $prefix*
}

main