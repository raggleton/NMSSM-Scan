#!/bin/bash

declare -a jobdirs=(
jobs_50_MICRO_28_Apr_15_1404
jobs_50_MICRO_28_Apr_15_2016
jobs_50_MICRO_28_Apr_15_2017
jobs_50_MICRO_28_Apr_15_2018
jobs_50_MICRO_28_Apr_15_2019
jobs_50_MICRO_28_Apr_15_2020
jobs_50_MICRO_28_Apr_15_2022
jobs_50_MICRO_28_Apr_15_2023
jobs_50_MICRO_28_Apr_15_2024
jobs_50_MICRO_28_Apr_15_2025
)

for f in "${jobdirs[@]}"
do
    echo $f
    if [ ! -d "data/$f" ]; then
        echo "Making dir"
        mkdir "data/$f"
    fi
    scp soolin:/hdfs/user/ra12451/NMSSM-Scan/$f/output*.dat data/$f/
done
