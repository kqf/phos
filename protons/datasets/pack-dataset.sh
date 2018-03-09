archive="LHC17.tar.gz"
pattern="LHC17?-pass1.txt"
prefix="verified-"


function main(){
	# Clean the directory
	rm $prefix*

	# Add comas at the end of each file
	for file in $(ls $pattern); do
		echo $file
		sed '$!s/$/,/' $file > tmp-$prefix$file
		(tr -d '\n' < tmp-$prefix$file)>>$prefix$file
		rm tmp-$prefix$file
	done

	tar czvf $archive $prefix*
	rm $prefix*
}

main