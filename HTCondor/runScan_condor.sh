#!/bin/bash -e
which gfortran
# For running on HTCondor
# TODO: use getopts
echo "Running with parameters: $@"
# parameters are: [job dir to put output] [batch number] [number of points]
jobdir=$1
batchNum=$2
numPoints=$3

# choose whether to run with extra programs
doSuperIso=0
doNMSSMCalc=0
doHiggsBounds=1
doHiggsSignals=1
doSushi=0

# Versions
NTVER="4.9.1"
HBVER="4.3.1"
HSVER="1.4.0"

# Setup NMSSMTools
# -----------------------------------------------------------------------------
tar xzf /hdfs/user/ra12451/NMSSM-Scan/zips/NMSSMTools_${NTVER}.tar.gz
cd NMSSMTools_${NTVER}
# patch bug in moving output files due to relpaths eurgh
# patch run < ../NT.patch
patch sources/micromegas/clean < ../NT_clean.patch
make clean
make init
make
cd ..

# Setup HiggsBounds
# -----------------------------------------------------------------------------
HBOPT=""
if [[ $doHiggsBounds == 1 ]]; then
    tar xzf /hdfs/user/ra12451/NMSSM-Scan/zips/HiggsBounds-${HBVER}.tar.gz
    HBOPT="--HB $PWD/HiggsBounds-${HBVER}"
    cd HiggsBounds-${HBVER}
    make clean
    # patch to remove spurious printout
    # patch HiggsBounds.F90 < ../HB.patch
    ./configure
    make
    cd ..
fi

# Setup Higgs Signals
# -----------------------------------------------------------------------------
HSOPT=""
if [[ $doHiggsSignals == 1 ]]; then
    tar xzf /hdfs/user/ra12451/NMSSM-Scan/zips/HiggsSignals-${HSVER}.tar.gz
    HSOPT="--HS $PWD/HiggsSignals-${HSVER}"
    cd HiggsSignals-${HSVER}
    make clean
    # patch to remove spurious printout
    patch datatables.f90 < ../HS_datatables.patch
    patch HiggsSignals_subroutines.F90 < ../HS_subroutines.patch
    # patch to assign mass better
    patch usefulbits_HS.f90 < ../HS_assignmass.patch
    ./configure
    make
    cd ..
fi

# Setup NMSSMCALC
# -----------------------------------------------------------------------------
if [[ $doNMSSMCalc == 1 ]]; then
    mkdir nmssmcalc
    tar -xvzf nmssmcalc.tar.gz -C nmssmcalc
    cd nmssmcalc
    make
    cd ..
    ls
fi

# Setup SusHi - BROKEN
# -----------------------------------------------------------------------------
# Need to tell it where LHAPDF is - check this is right!
# make sure that the gcc lhapdf was compiled against matches the version that
# gfortran was made with, otherwise you're gonna have a bad time
SUSHIOPT=""
if [[ $doSushi == 1 ]]; then
    SUSHIOPT="--sushi"
    tar xzf /hdfs/user/ra12451/NMSSM-Scan/zips/SusHi-1.5.0.tar.gz
    cd SusHi-*
    ./configure

    # # sed -i '0,/LHAPATH =/s@@LHAPATH = /cvmfs/sft.cern.ch/lcg/external/MCGenerators/lhapdf/5.8.9/x86_64-slc6-gcc46-opt/lib@' Makefile
    # sed -i '0,/LHAPATH =/s@@LHAPATH = /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf6/6.1.5/lib@' Makefile
    # make
    cd ..
fi

# Run NMSSMTools over parameter points
# -----------------------------------------------------------------------------
python NMSSMScan.py --card inp_*.dat -n $3 --param paramRange*.json --oDir . --NT NMSSMTools_${NTVER} $HBOPT $HSOPT $SUSHIOPT
# ls

# Setup SuperIso
# -----------------------------------------------------------------------------
if [[ $doSuperIso == 1 ]]; then
    tar -xvzf superiso_v*.tgz
    cd superiso*
    make slha
    # Run SuperIso over files and output screen info to file
    for s in ../spectr*.dat;
    do
        id=`basename $s`
        id=${id%.dat}
        id=${id#spectr}
        ./slha.x $s > ../superiso$id.dat
    done
    cd ..
    ls
fi

# Save space - delete useless files
# -----------------------------------------------------------------------------
for f in $(grep -l "M_A1^2<1" spectr*.dat);
do
    echo "rm $f"
    rm $f
done

for f in $(grep -l "M_H1^2<1" spectr*.dat);
do
    echo "rm $f"
    rm $f
done

for f in $(grep -l "M_HC^2<1" spectr*.dat);
do
    echo "rm $f"
    rm $f
done

rm omega*

# Zip up files to transfer to HDFS
# -----------------------------------------------------------------------------
nfiles=`ls spectr*.dat | wc -l`
echo "Zipping up $nfiles files"
tar -cvzf "spectr${batchNum}.tgz" spectr*.dat
cp "spectr${batchNum}.tgz" "$jobdir"

# tar -cvzf "omega${batchNum}.tgz" omega*.dat
# cp "omega${batchNum}.tgz" "$jobdir"

if [[ $doSuperIso == 1 ]]; then
    tar -cvzf $jobdir/superiso$batchNum.tgz superiso*.dat
    cp "$jobdir/superiso$batchNum.tgz" "$jobdir"
fi
if [[ $doNMSSMCalc == 1 ]]; then
    tar -cvzf $jobdir/nmssmcalc$batchNum.tgz nmssmcalc_*.dat
    cp "$jobdir/nmssmcalc$batchNum.tgz" "$jobdir"
fi

# ls