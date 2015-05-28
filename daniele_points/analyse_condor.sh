#!/bin/bash

# For running on HTcondor
# ASSUMES THAT THE DIR EXISTS ON /hdfs
# Args: <dir with spectrum files> <process ID for uniqueness>

hdfsdir=/hdfs/user/ra12451/NMSSM-Scan/$1
if [ ! -d $hdfsdir ]; then
    echo "Cannot find dir $hdfsdir"
else
    # run perl analysis script over files
    perl Analyse_scans.pl $hdfsdir $hdfsdir $2
fi