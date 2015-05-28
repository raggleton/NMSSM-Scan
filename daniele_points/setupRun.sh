#!/bin/bash
# Special version to do daniele scan poitns - already have input cards
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [job dir to put output] [batch number]
jobdir=$1
batchNum=$2

###################
# Setup NMSSMTools
###################
tar -xvzf NMSSMTools_*.tgz
cd NMSSMTools_*
# patch bug in moving output files due to relpaths eurgh
patch run < ../run.patch
make init
make

###################
# Run NMSSMTools over parameter points
# Do a batch of 5000
###################
start=$(($batchNum * 5000))
limit=$(((($batchNum+1)*5000)-1))
python /hdfs/user/ra12451/NMSSM-Scan/daniele_points/read_daniele_csv.py $start $limit
for ((a=$start; a <= $limit ; a++))
do
    ./run /hdfs/user/ra12451/NMSSM-Scan/daniele_points/inp_$a.dat
    rm /hdfs/user/ra12451/NMSSM-Scan/daniele_points/inp_$a.dat
done
ls

###################
# Zip up files to transfer back
###################
# tar -cvzf /hdfs/users/ra12451/NMSSM-scan/daniele_points/spectr$batchNum.tgz spectr*.dat paramRange.txt NMSSM_scan.pl
# tar -cvzf /hdfs/users/ra12451/NMSSM-scan/daniele_points/omega$batchNum.tgz omega*.dat

###################
# Tidy up
###################
# rm spectr*.dat
# rm omega*.dat
cd ..
rm NMSSMTools_*.tgz
rm -r NMSSMTools_*
