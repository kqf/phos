#!/bin/bash

# set job and simulation variables as :
COMMAND_HELP="./dpgsim.sh --mode <mode> --run <run> --generator <generatorConfig> --energy <energy> --system <system> --particle <partPDG> --detector <detectorConfig> --magnet <magnetConfig> --simulation <simulationConfig> --reconstruction <reconstructionConfig> --uid <uniqueID> --nevents <numberOfEvents> --qa <qaConfig> --aod <aodConfig>"

function runcommand(){
    echo -e "\n"
    echo -e "\n" >&2

    echo "* $1 : $2"
    echo "* $1 : $2" >&2

    START=`date "+%s"`
    time aliroot -b -q -x $2 >>$3 2>&1
    exitcode=$?
    END=`date "+%s"`
    echo "$1 TIME: $((END-START))"
    
    expectedCode=${5-0}
    
    if [ "$exitcode" -ne "$expectedCode" ]; then
        echo "*! $2 failed with exitcode $exitcode, expecting $expectedCode"
        echo "*! $2 failed with exitcode $exitcode, expecting $expectedCode" >&2
        echo "$2 failed with exitcode $exitcode, expecting $expectedCode" >> validation_error.message
        exit ${4-$exitcode}
    else
        echo "* $2 finished with the expected exit code ($expectedCode), moving on"
        echo "* $2 finished with the expected exit code ($expectedCode), moving on" >&2
    fi

}

function runBenchmark(){
    if [ ! -x "$ROOTSYS/test/stressHepix" ]; then
        (cd "$ROOTSYS/test" && make) &>/dev/null
    fi

    if [ ! -x "$ROOTSYS/test/stressHepix" ]; then
        echo "ERROR: No stressHepix in this ROOT package : $ROOTSYS"
    else
        $ROOTSYS/test/stress -b &> /dev/null
        $ROOTSYS/test/stress -b &> stress.output
        FOOTER=`cat stress.output | tail -n6`

        ROOTMARKS=`echo "$FOOTER" | grep ROOTMARKS  | cut -d= -f2 | cut '-d*' -f1`

        ROOTVER=`echo "$FOOTER" | grep ROOTMARKS  | cut -d= -f2 | cut '-d*' -f2`

        read REALTIME CPUTIME < <(echo "$FOOTER" | grep "Real Time" | awk '{print $6 " " $11}')

        if [ -z "$ROOTMARKS" ]; then
            echo "ERROR: empty output of stressHepix"
        else
            echo "ROOTMARKS : $ROOTMARKS"
            echo "ROOTVER : $ROOTVER"
            echo "Real time : $REALTIME"
            echo "CPU time : $CPUTIME"
        fi

        rm stress.output
    fi

    grep "model name" /proc/cpuinfo | uniq -c
    
    if [ -x /cvmfs/atlas.cern.ch/repo/benchmarks/htcondor/x86_64/slc6/stripped/8.2.8/libexec/condor_kflops ]; then
        /cvmfs/atlas.cern.ch/repo/benchmarks/htcondor/x86_64/slc6/stripped/8.2.8/libexec/condor_kflops &>/dev/null
        /cvmfs/atlas.cern.ch/repo/benchmarks/htcondor/x86_64/slc6/stripped/8.2.8/libexec/condor_kflops
    else
        echo "kFlops executable is not available on `hostname -f`"
    fi
    
    if [ -f lhcb.py ]; then
        python lhcb.py
    fi
}

# Define the pt hard bin arrays
pthardbin_loweredges=( 0 5 11 21 36 57 84 117 152 191 234 )
pthardbin_higheredges=( 5 11 21 36 57 84 117 152 191 234 -1)

CONFIG_NEVENTS="200"
CONFIG_SEED=""
CONFIG_GENERATOR=""
CONFIG_MAGNET=""
CONFIG_ENERGY=""
CONFIG_SYSTEM=""
CONFIG_PARTICLE="111"
CONFIG_TRIGGER=""
CONFIG_DETECTOR=""
CONFIG_PHYSICSLIST=""
CONFIG_BMIN=""
CONFIG_BMAX=""
CONFIG_PTHARDBIN=""
CONFIG_PTHARDMIN=""
CONFIG_PTHARDMAX=""
CONFIG_QUENCHING=""
CONFIG_RUN=""
CONFIG_UID="1"
CONFIG_SIMULATION=""
CONFIG_RECONSTRUCTION=""
CONFIG_QA=""
CONFIG_AOD=""
CONFIG_MODE="full"

RUNMODE=""

while [ ! -z "$1" ]; do
    option="$1"
    shift
    
    if [ "$option" = "--mode" ]; then
	CONFIG_MODE="$1"
	export CONFIG_MODE
        shift
    elif [ "$option" = "--run" ]; then
	CONFIG_RUN="$1"
	export CONFIG_RUN
        shift
    elif [ "$option" = "--uid" ]; then
        CONFIG_UID="$1"
	export CONFIG_UID
        shift
    elif [ "$option" = "--generator" ]; then
        CONFIG_GENERATOR="$1"
	export CONFIG_GENERATOR
        shift
    elif [ "$option" = "--magnet" ]; then
        CONFIG_MAGNET="$1"
	export CONFIG_MAGNET	
        shift
    elif [ "$option" = "--detector" ]; then
        CONFIG_DETECTOR="$1"
	export CONFIG_DETECTOR
        shift
    elif [ "$option" = "--system" ]; then
        CONFIG_SYSTEM="$1"
	export CONFIG_SYSTEM
        CONFIG_TRIGGER="$1"
	export CONFIG_TRIGGER
        shift
    elif [ "$option" = "--particle" ]; then
        CONFIG_PARTICLE="$1"
	export CONFIG_PARTICLE
        shift
    elif [ "$option" = "--energy" ]; then
        CONFIG_ENERGY="$1"
	export CONFIG_ENERGY
        shift
    elif [ "$option" = "--simulation" ]; then
        CONFIG_SIMULATION="$1"
	export CONFIG_SIMULATION
        shift
    elif [ "$option" = "--reconstruction" ]; then
        CONFIG_RECONSTRUCTION="$1"
	export CONFIG_RECONSTRUCTION
        shift
    elif [ "$option" = "--qa" ]; then
        CONFIG_QA="$1"
	export CONFIG_QA
        shift
    elif [ "$option" = "--aod" ]; then
        CONFIG_AOD="$1"
	export CONFIG_AOD
        shift
    elif [ "$option" = "--physicslist" ]; then
        CONFIG_PHYSICSLIST="$1"
	export CONFIG_PHYSICSLIST
        shift
    elif [ "$option" = "--bmin" ]; then
        CONFIG_BMIN="$1"
	export CONFIG_BMIN
        shift
    elif [ "$option" = "--bmax" ]; then
        CONFIG_BMAX="$1"
	export CONFIG_BMAX
        shift
    elif [ "$option" = "--pthardbin" ]; then
        CONFIG_PTHARDBIN="$1"
	export CONFIG_PTHARDBIN
        shift  
    elif [ "$option" = "--quench" ]; then
        CONFIG_QUENCHING="$1"
	export CONFIG_QUENCHING
        shift 
    elif [ "$option" = "--nevents" ]; then
        CONFIG_NEVENTS="$1"
	export CONFIG_NEVENTS
        shift 
    elif [ "$option" = "--sdd" ]; then
        RUNMODE="SDD"
	export RUNMODE
    fi
done

DC_RUN=$CONFIG_RUN
DC_EVENT=$CONFIG_UID
export DC_RUN DC_EVENT

CONFIG_SEED=$((ALIEN_PROC_ID%1000000000))
if [ "$CONFIG_SEED" -eq 0 ]; then
    CONFIG_SEED=$(((CONFIG_RUN*100000+CONFIG_UID)%1000000000))
    CONFIG_SEED_BASED="run / unique-id : $CONFIG_RUN / $CONFIG_UID"
else
    CONFIG_SEED_BASED="AliEn job ID"
fi
export CONFIG_SEED

if [ "$CONFIG_SEED" -eq 0 ]; then
    echo "*!  WARNING! Seeding variable for MC is 0 !" >&2
fi

if [ ! -z "$CONFIG_PTHARDBIN" ]; then
    # Define environmental vars for pt binning
    CONFIG_PTHARDMIN=${pthardbin_loweredges[$CONFIG_PTHARDBIN]}
    CONFIG_PTHARDMAX=${pthardbin_higheredges[$CONFIG_PTHARDBIN]}
    export CONFIG_PTHARDMIN CONFIG_PTHARDMAX

    echo "* pt hard from $CONFIG_PTHARDMIN to $CONFIG_PTHARDMAX"
fi

mkdir input
mv galice.root ./input/galice.root
mv Kinematics.root ./input/Kinematics.root
ls input

export ALIMDC_RAWDB1="./mdc1"
export ALIMDC_RAWDB2="./mdc2"
export ALIMDC_TAGDB="./mdc1/tag"
export ALIMDC_RUNDB="./mdc1/meta"

export PYTHIA8DATA="$ALICE_ROOT/PYTHIA8/pythia8/xmldoc"
export LHAPDF="$ALICE_ROOT/LHAPDF"
export LHAPATH="$ALICE_ROOT/LHAPDF/PDFsets"

if [ -f "$G4INSTALL/bin/geant4.sh" ]; then
    echo "* Sourcing G4 environment from $G4INSTALL/bin/geant4.sh"
    source $G4INSTALL/bin/geant4.sh
fi

### check whether we are in OCDB generation job 

if [[ $ALIEN_JDL_LPMOCDBJOB == "true" ]]; then
    echo ">>>>> OCDB generation: force MODE to 'ocdb'"
    export CONFIG_MODE="ocdb"
fi
    
### check basic requirememts
    
    if [[ $CONFIG_MODE == "" ]]; then
	echo ">>>>> ERROR: mode is required!"
	echo $COMMAND_HELP
	exit 2
    fi

if [[ $CONFIG_RUN == "" ]]; then
    echo ">>>>> ERROR: run number is required!"
    echo $COMMAND_HELP
    exit 2
fi

### automatic settings from CONFIG_MODE

if [[ $CONFIG_MODE == *"Muon"* ]]; then
    if [[ $CONFIG_DETECTOR == "" ]]; then
	export CONFIG_DETECTOR="Muon"
    fi
    if [[ $CONFIG_SIMULATION == "" ]]; then
	export CONFIG_SIMULATION="Muon"
    fi
    if [[ $CONFIG_RECONSTRUCTION == "" ]]; then
	export CONFIG_RECONSTRUCTION="Muon"
    fi
    if [[ $CONFIG_QA == "" ]]; then
	export CONFIG_QA="Muon"
    fi
    if [[ $CONFIG_AOD == "" ]]; then
	export CONFIG_AOD="Muon"
    fi
fi

##########################################

echo
echo "============================================"
echo " DPGSIM"
echo "============================================"
echo "Mode............. $CONFIG_MODE"
echo "Run.............. $CONFIG_RUN"
echo "Unique-ID........ $CONFIG_UID"
echo "MC seed.......... $CONFIG_SEED (based on $CONFIG_SEED_BASED)"
echo "No. Events....... $CONFIG_NEVENTS"
echo "Generator........ $CONFIG_GENERATOR"
echo "System........... $CONFIG_SYSTEM"
echo "Particle......... $CONFIG_PARTICLE"
echo "Trigger.......... $CONFIG_TRIGGER"
echo "Energy........... $CONFIG_ENERGY"
echo "Detector......... $CONFIG_DETECTOR"
echo "Simulation....... $CONFIG_SIMULATION"
echo "Reconstruction... $CONFIG_RECONSTRUCTION"
echo "QA train......... $CONFIG_QA"
echo "AOD train........ $CONFIG_AOD"
echo "B-field.......... $CONFIG_MAGNET"
echo "Physicslist...... $CONFIG_PHYSICSLIST"
echo "b-min............ $CONFIG_BMIN"
echo "b-max............ $CONFIG_BMAX"
echo "pT hard bin...... $CONFIG_PTHARDBIN"
echo "============================================"
echo

### createSnapshot.C

if [[ $CONFIG_MODE == *"ocdb"* ]]; then

    OCDBC=Sim/CreateSnapshot.C
    if [ -f CreateSnapshot.C ]; then
	SIMC=CreateSnapshot.C
    fi
    
    runcommand "OCDB SIM SNAPSHOT" $OCDBC\(0\) ocdbsim.log 500
    mv -f syswatch.log ocdbsimwatch.log
    if [ ! -f OCDBsim.root ]; then
	echo "*! Could not find OCDBsim.root, the snapshot creation chain failed!"
	echo "Could not find OCDBsim.root, the snapshot creation chain failed!" >> validation_error.message
	exit 2
    fi

    runcommand "OCDB REC SNAPSHOT" $OCDBC\(1\) ocdbrec.log 500
    mv -f syswatch.log ocdbrecwatch.log
    if [ ! -f OCDBrec.root ]; then
	echo "*! Could not find OCDBrec.root, the snapshot creation chain failed!"
	echo "Could not find OCDBrec.root, the snapshot creation chain failed!" >> validation_error.message
	exit 2
    fi

fi

### sim.C

if [[ $CONFIG_MODE == *"sim"* ]] || [[ $CONFIG_MODE == *"full"* ]]; then
    
    if [[ $CONFIG_GENERATOR == "" ]]; then
	echo ">>>>> ERROR: generator is required for full production mode!"
	echo $COMMAND_HELP
	exit 2
    fi

    if [[ $CONFIG_SYSTEM == "" ]]; then
	echo ">>>>> ERROR: system is required for full production mode!"
	echo $COMMAND_HELP
	exit 2
    fi

    SIMC=Sim/sim.C
    if [ -f sim.C ]; then
	SIMC=sim.C
    fi
    
    runcommand "SIMULATION" $SIMC sim.log 5
    mv -f syswatch.log simwatch.log

    runBenchmark

fi

### rec.C

if [[ $CONFIG_MODE == *"rec"* ]] || [[ $CONFIG_MODE == *"full"* ]]; then

    RECC=Sim/rec.C
    if [ -f rec.C ]; then
	RECC=rec.C
    fi
    
    runcommand "RECONSTRUCTION" $RECC rec.log 10
    mv -f syswatch.log recwatch.log    
    if [ ! -f AliESDs.root ]; then
	echo "*! Could not find AliESDs.root, the simulation/reconstruction chain failed!"
	echo "Could not find AliESDs.root, the simulation/reconstruction chain failed!" >> validation_error.message
	exit 2
    fi

#     CHECKESDC=Sim/CheckESD.C
#     if [ -f CheckESD.C ]; then
# 	CHECKESDC=CheckESD.C
#     fi    
#     runcommand "CHECK ESD" $CHECKESDC check.log 60 1
#     rm -f *.RecPoints.root *.Hits.root *.Digits.root *.SDigits.root

fi

### QAtrainsim.C

if [[ $CONFIG_MODE == *"qa"* ]] || [[ $CONFIG_MODE == *"full"* ]]; then
    
    echo "QAresults.root" >> validation_extrafiles.list

    QATRAINSIMC=$ALIDPG_ROOT/QA/QAtrainsim.C\($CONFIG_RUN\)
    if [ -f QAtrainsim.C ]; then
	QATRAINSIMC=QAtrainsim.C\($CONFIG_RUN\)
    fi
    
    runcommand "QA TRAIN" $QATRAINSIMC qa.log 1000
    mv -f syswatch.log qawatch.log

    for file in *.stat; do
	mv -f "$file" "$file.qa"
    done
    
fi

### AODtrainsim.C

if [[ $CONFIG_MODE == *"aod"* ]] || [[ $CONFIG_MODE == *"full"* ]]; then

    echo "AliAOD.root" >> validation_extrafiles.list
    
    AODTRAINSIMC=Sim/CreateAOD.C
    if [ -f CreateAOD.C ]; then
	AODTRAINSIMC=AODtrainsim.C
    fi

    rm -f outputs_valid &>/dev/null

    runcommand "AOD TRAIN" $AODTRAINSIMC aod.log 1000
    mv -f syswatch.log aodwatch.log

    for file in *.stat; do
	mv -f $file $file.aod
    done
    
fi


exit 0
