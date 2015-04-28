#!/bin/bash
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [batch number]

# Setup NMSSMTools on execute machine
tar -xvzf NMSSMTools_4.5.1.tgz
cd NMSSMTools_4.5.1
# patch bug in mving output files
patch run < ../run.patch
make init
make
ls
cd ..

# Run NMSSMTools over parameter points
perl NMSSM_scan.pl $1

ls
# Zip up spectrum files to transfer back
tar -cvzf spectr$1.tgz spectr*.dat paramRange.txt