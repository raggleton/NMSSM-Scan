#!/bin/bash

# For running on HTcondor
# ASSUMES THAT THE DIR EXISTS ON /hdfs
# Args: <dir with spectrum files> <process ID for uniqueness>

hdfsdir=/hdfs/user/ra12451/NMSSM-Scan/$1
if [ ! -d $hdfsdir ]; then
    echo "Cannot find dir $hdfsdir"
else
    # Make a dir on the worker node with the same name
    # Extract all files into that new dir
    if [ ! -d $1 ]; then
        mkdir $1
    fi
    tar -xvzf $hdfsdir/spectr$2.tgz -C $1

    # Check if superiso output exists. If not, we will have to make them -
    # for legacy folders before SuperIso was implemented
    # If you don't want it, comment this part out - the analysis script
    # will still run fine
    if [ ! -e $hdfsdir/superiso$2.tgz ]; then
        echo "Running SuperIso"
        tar -xvzf superiso_v*.tgz
        cd superiso*
        make slha
        # Run SuperIso over files and output screen info to file
        for s in ../$1/spectr*.dat;
        do
            siName=${s/spectr/superiso}
            echo $siName
            ./slha.x $s > $siName
        done
        cd ../$1
        tar -cvzf $hdfsdir/superiso$2.tgz superiso*.dat
        cd ..
    else
        tar -xvzf $hdfsdir/superiso$2.tgz -C $1
    fi
    ls

    # run perl script over them
    perl Analyse_scans.pl $1 $hdfsdir $2

    # cleanup
    rm -r $1
fi