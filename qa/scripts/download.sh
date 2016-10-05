function download_from_grid()
{
	counter=1
    MHOME=/alice/cern.ch/user/o/okovalen

    # for run in $$(alien_ls /$(MPATH) | grep 000);do alien_cp alien://$(MPATH)/$$run/AnalysisResults.root $(PERIOD)/$$run.root; done
	for run in $(alien_ls $MHOME/$1/output | grep 000) 
	do 
		echo $run
		until alien_cp alien://$MHOME/$1/output/$run/$2 $3/$((counter++)).$run.root; do echo 'Trying again in 10 sec.'; sleep 10; done
	done
}

download_from_grid $1 $2 $3
