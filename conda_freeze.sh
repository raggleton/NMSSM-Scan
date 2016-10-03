#!/bin/bash -e

# Use the yaml: conda env create -f conda_scans.yml
conda env export > conda_scans.yml

# Use the txt: conda create --name scans --file conda_scnas.txt
# conda list --export > conda_scans.txt

