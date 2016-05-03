#!/bin/bash -e
conda list --export > conda_pandas.txt
conda env export > conda_pandas.yml

