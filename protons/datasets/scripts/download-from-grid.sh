
# Run this code inside /data folder
# for i in {001..010}; do
# 	mkdir -p $datapath/$i/
# 	alien_cp alien://alice/data/$datapath/$i/AliAOD.root $datapath/$i/AliAOD.root
# done

for run in 257684 257685 257687 257688 257689 257692 257697 257724 257725; do
	datapath=2016/LHC16k/000$run/pass1/AOD/001/
	mkdir -p $datapath/
	alien_cp alien://alice/data/$datapath/AliAOD.root $datapath/AliAOD.root
done
