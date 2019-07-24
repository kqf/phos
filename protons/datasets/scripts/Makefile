archive = PHOS-LHC18.tar.gz
pattern = "../LHC18?-pass1.txt"

diff:
	./diff-datasets.sh
	tar zcvf diff-lhc16.tar.gz  diff-*.txt 
	wc -l diff-*.txt
	rm diff-*.txt

pack:
	./pack-dataset.sh $(archive) $(pattern)
