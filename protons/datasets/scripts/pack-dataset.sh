archive=$1
pattern=$2
# pattern="LHC17?-pass1.txt"


function main(){
	# Add comas at the end of each file
	for file in $pattern; do
		echo $file
		sed '$!s/$/, /' $file | sed 's/^0*//' > $file.tmp
		(tr -d '\n' < $file.tmp)>>$file.verified
		rm $file.tmp
	done

	tar czvf $archive $pattern.verified
	rm $pattern.verified
}

main
