year=2018
name=iteration1
train=908_20190724-1352 
ofilename=CaloCellsQA.root

declare -A runlist=([1]=5 [2]=5 [3]=5 [4]=5 [5]=5 [6]=5 [7]=5 [8]=5 [9]=5 [10]=5 [11]=5 [12]=5 [13]=5, [14]=5)
declare -A names=([1]=LHC18b [2]=LHC18d [3]=LHC18e [4]=LHC18f [5]=LHC18g [6]=LHC18h [7]=LHC18i [8]=LHC18j [9]=LHC18k [10]=LHC18l [11]=LHC18m [12]=LHC18n [13]=LHC18o [14]=LHC18p)

function main()
{
    for child in ${!runlist[@]}; do
        period=${names[$child]}
        make ${makeoption} child=${child} period=${period} \
            ofilename=${ofilename} \
            year=${year} \
            name=${name} \
            train=${train}
    done
}

main
