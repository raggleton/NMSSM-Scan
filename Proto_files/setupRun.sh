#!/bin/bash
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [batch number]

# Setup NMSSMTools on execute machine
tar -xvzf NMSSMTOOLS.tgz
ls

# Run NMSSMTools over parameter points
perl NMSSM_scan.pl

# Zip up spectrum files to transfer back
tar -cvzf spectr$1.tgz spectr*.dat paramRange.txt