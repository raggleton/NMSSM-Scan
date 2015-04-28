#!/bin/bash

# For running on HTcondor
# ASSUMES THAT THE DIR EXISTS ON /hdfs
# Args: <dir with spectrum files> <process ID for uniqueness>

hdfsdir=/hdfs/user/ra12451/NMSSM-Scan/$1
if [ ! -d $hdfsdir ]; then
    echo "Cannot find dir $hdfsdir"
else
    # Make a dir on the worker node with the same name
    # Extract the spectr.tgz into that new dir
    if [ ! -d $1 ]; then
        mkdir $1
    fi
    tar -xvzf $hdfsdir/spectr$2.tgz -C $1
    ls
    # run perl script over them
    perl Analyse_scans.pl $1 $hdfsdir $2
    rm -r $1
fi