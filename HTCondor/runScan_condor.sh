#!/bin/bash
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [job dir to put output] [batch number] [number of points]
jobdir=$1
batchNum=$2
numPoints=$3

# Setup NMSSMTools
# -----------------------------------------------------------------------------
tar -xzf /hdfs/user/ra12451/NMSSM-Scan/zips/NMSSMTools_*.tgz
cd NMSSMTools_*
# patch bug in moving output files due to relpaths eurgh
patch run < ../NT.patch
make init
make
cd ..
# ls

# Setup HiggsBounds
# -----------------------------------------------------------------------------
tar -xzf /hdfs/user/ra12451/NMSSM-Scan/zips/HiggsBounds-*.tar.gz
cd HiggsBounds-*
# patch to remove spurious printout
patch HiggsBounds.F90 < ../HB.patch
./configure
make
cd ..

# Setup NMSSMCALC
# -----------------------------------------------------------------------------
# mkdir nmssmcalc
# tar -xvzf nmssmcalc.tar.gz -C nmssmcalc
# cd nmssmcalc
# make
# cd ..
# ls

# Setup SusHi - BROKEN
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# First arg is job dir - where the input.dat and spectr.dat files get made
# perl NMSSM_scan.pl $PWD $2
cp "${jobdir}/inp_PROTO.dat" "inp_${batchNum}.dat"
cp "${jobdir}/paramRange.json" paramRange.json
cp "${jobdir}/NMSSMScan.py" NMSSMScan.py
cp "${jobdir}/common_utils.py" common_utils.py
python NMSSMScan.py --card "inp_${batchNum}.dat" -n $3 --param paramRange.json --oDir .
ls
# Setup SuperIso
# -----------------------------------------------------------------------------
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

# Zip up files to transfer back
# -----------------------------------------------------------------------------
tar -cvzf "spectr${batchNum}.tgz" spectr*.dat
cp "spectr${batchNum}.tgz" "$jobdir"
tar -cvzf "omega${batchNum}.tgz" omega*.dat
cp "omega${batchNum}.tgz" "$jobdir"
# tar -cvzf $jobdir/superiso$batchNum.tgz superiso*.dat
# tar -cvzf $jobdir/nmssmcalc$batchNum.tgz nmssmcalc_*.dat

ls

# Tidy up
# -----------------------------------------------------------------------------
rm *.dat
rm *.patch
rm *.py
rm *.json
rm *.tgz
rm *.tar.gz
rm -rf NMSSMTools*
rm -rf HiggsBounds*
rm -rf nmssmcalc*
rm -rf superiso*