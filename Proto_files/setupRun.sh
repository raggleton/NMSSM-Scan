#!/bin/bash
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [job dir to put output] [batch number]
jobdir=$1
batchNum=$2

###################
# Setup NMSSMTools
###################
tar -xvzf NMSSMTools_*.tgz
cd NMSSMTools_*
# patch bug in moving output files due to relpaths eurgh
patch run < ../run.patch
make init
make
cd ..
# ls

###################
# Setup NMSSMCALC
###################
mkdir nmssmcalc
tar -xvzf nmssmcalc.tar.gz -C nmssmcalc
cd nmssmcalc
make
cd ..
# ls

###################
# Setup SusHi - BROKEN
###################
# Need to tell it where LHAPDF is - check this is right!
# make sure that the gcc lhapdf was compiled against matches the version that
# gfortran was made with, otherwise you're gonna have a bad time
# tar -xvzf SusHi-1.5.0.tar.gz
# cd SusHi-1.5.0
# ./configure
# # sed -i '0,/LHAPATH =/s@@LHAPATH = /cvmfs/sft.cern.ch/lcg/external/MCGenerators/lhapdf/5.8.9/x86_64-slc6-gcc46-opt/lib@' Makefile
# sed -i '0,/LHAPATH =/s@@LHAPATH = /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/lhapdf6/6.1.5/lib@' Makefile
# make
# cd ..

# Run NMSSMTools over parameter points
# First arg is job dir - where the input.dat and spectr.dat files get made
perl NMSSM_scan.pl $PWD $2

###################
# Setup SuperIso
###################
# tar -xvzf superiso_v*.tgz
# cd superiso*
# make slha
# # Run SuperIso over files and output screen info to file
# for s in ../spectr*.dat;
# do
#     id=`basename $s`
#     id=${id%.dat}
#     id=${id#spectr}
#     ./slha.x $s > ../superiso$id.dat
# done
# cd ..
# ls

ls

###################
# Zip up files to transfer back
###################
tar -cvzf $jobdir/spectr$batchNum.tgz spectr*.dat paramRange.txt NMSSM_scan.pl
tar -cvzf $jobdir/omega$batchNum.tgz omega*.dat
# tar -cvzf $jobdir/superiso$batchNum.tgz superiso*.dat
tar -cvzf $jobdir/nmssmcalc$batchNum.tgz nmssmcalc_*.dat

###################
# Tidy up
###################
rm spectr*.dat
rm omega*.dat
# rm superiso*.dat
rm NMSSMTools_*.tgz
rm nmssmcalc.tar.gz
rm -r nmssmcalc
rm -r NMSSMTools_*
# rm -r superiso*