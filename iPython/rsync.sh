#!/bin/bash

# Synchronise this folder with Dropbox, leaving out big hdf5 files
rsync -avzP --exclude=*.csv --exclude=*.h5 ~/NMSSM-Scan/iPython/ ~/Dropbox/NMSSM-Scan/iPython/
