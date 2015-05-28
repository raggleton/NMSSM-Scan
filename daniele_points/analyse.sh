#!/bin/bash

# Setup and run a load of analysis scripts for various folders with spectr*.tgz
# in the corresponding hdfs folder
#
# Usage:
#
#   ./analysis.sh dir1 dir2 dir3
#

for f in $@
do
    echo $f
    NJOBS=`ls /hdfs/user/ra12451/NMSSM-Scan/$f/spectr*.tgz | wc -l`
    # make condor script for this dir
    cp Proto_files/analyse.condor $f/analyse.condor
    sed -i "s@SEDJOBDIR@$f@g" $f/analyse.condor
    sed -i "s/SEDNUM/$NJOBS/g" $f/analyse.condor
    condor_submit $f/analyse.condor
    # give it a pause so you don't clog up the queue - analysis jobs should run v.quickly
    sleep 60
done
