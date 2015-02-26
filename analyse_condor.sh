#!/bin/bash

# For running on HTcondor

# make dir with same name as locally, put spectrum files there
echo "Making dir $1"
mkdir $1
for f in *.tgz; do tar -xvzf *.tgz -C $1; done
# run perl script over them
perl Analyse_scans.pl $1 $2