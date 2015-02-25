#!/bin/bash

# For running locally.
# DON'T do with lots of files, it takes ages and you'll be rounded up and shot
# To run on HTcondor, see analyse_condor.sh

for f in "$@"
do
	perl Analyse_scans.pl "$f"&
done
