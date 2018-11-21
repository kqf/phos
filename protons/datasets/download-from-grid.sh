export datapath=2016/LHC16k/000257682/pass1/AOD/

# Run this code inside /data folder
for i in {001..010}; do
	mkdir -p $datapath/$i/
	alien_cp alien://alice/data/$datapath/$i/AliAOD.root $datapath/$i/AliAOD.root
done
