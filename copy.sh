#!/bin/bash

declare -a jobdirs=(
jobs_50_MICRO_SCAN_M3MQ3MU3MD3AU3_14_May_15_1151
jobs_50_MICRO_SCAN_M3MQ3MU3MD3AU3AD3_14_May_15_1153
jobs_50_MICRO_SCAN_M3MQ3MU3AU3_13_May_15_1351
jobs_50_MICRO_SCAN_M3MQ3MU3AU3_06_May_15_1600
jobs_50_MICRO_SCAN_M3MQ3MU3AU3_12_May_15_1500
jobs_50_MICRO_DEFAULTMASS_SCAN_M3MQ3MU3AU3_06_May_15_1940
jobs_50_MICRO_DEFAULTMASS_SCAN_M3MQ3MU3AU3_06_May_15_2203
jobs_50_MICRO_DEFAULTMASS_SCAN_M3MQ3MU3AU3_06_May_15_2132
jobs_50_MICRO_DEFAULTMASS_SCAN_M3MQ3MU3AU3_12_May_15_1413
)

for f in "${jobdirs[@]}"
do
    echo $f
    if [ ! -d "data/$f" ]; then
        echo "Making dir"
        mkdir "data/$f"
    fi
    # Make this friendly - ensure it is nice'd and limit bandwidth
    rsync -avzP --rsync-path="nice rsync" --bwlimit=1000 --exclude=output_good* soolin:/hdfs/user/ra12451/NMSSM-Scan/$f/output*.dat data/$f/
done
