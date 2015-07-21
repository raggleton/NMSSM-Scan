#!/bin/bash
# This script is for the condor worker node
# to run make_hdf5.py

export PATH=/software/miniconda/envs/pandas/bin:/software/miniconda/bin:$PATH

source activate pandas
echo "Running with args: "$@
python make_hdf5.py $@
