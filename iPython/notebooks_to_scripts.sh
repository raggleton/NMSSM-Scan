#!/bin/bash -e

for n in *.ipynb; do
    echo $n
    jupyter nbconvert --to python "$n"
done