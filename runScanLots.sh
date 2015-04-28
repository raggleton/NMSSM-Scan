#!/bin/bash
#
# Helper script to run several sets of scan jobs, 
# without having to remember the 1 min wait

for i in {1..6};
do
    ./runScan.sh
    sleep 60
done
