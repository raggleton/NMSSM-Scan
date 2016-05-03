#!/bin/bash -e

# For running on HTcondor
# ASSUMES THAT THE DIRECTORY WITH SPECTRUM FILES EXISTS ON /hdfs
# Args: <dir with spectrum files> <process ID for uniqueness>
SPECTRDIR="$1"
PID="$2"

# Check if the directory on hdfs exists
# -----------------------------------------------------------------------------
hdfsdir=/hdfs/user/${LOGNAME}/NMSSM-Scan/"$SPECTRDIR"
if [ ! -d $hdfsdir ]; then
    echo "Cannot find dir $hdfsdir"
    exit 1
fi

# Make a dir on the worker node with the same name, extract spectrum files there
# -----------------------------------------------------------------------------
if [ ! -d "$SPECTRDIR" ]; then
    mkdir "$SPECTRDIR"
fi
tar -xzf $hdfsdir/spectr"$PID".tgz -C "$SPECTRDIR"

# Check if superiso output exists. If so, untar.
# -----------------------------------------------------------------------------
# If not, we will have to make them -
# for legacy folders before SuperIso was implemented
# If you don't want it, comment this part out - the analysis script
# will still run fine
# if [ ! -e $hdfsdir/superiso"$PID".tgz ]; then
#     echo "Running SuperIso"
#     tar -xvzf superiso_v*.tgz
#     cd superiso*
#     make slha
#     # Run SuperIso over files and output screen info to file
#     for s in ../"$SPECTRDIR"/spectr*.dat;
#     do
#         siName=${s/spectr/superiso}
#         echo $siName
#         ./slha.x $s > $siName
#     done
#     cd ../"$SPECTRDIR"
#     tar -cvzf $hdfsdir/superiso"$PID".tgz superiso*.dat
#     cd ..
# else
#     tar -xvzf $hdfsdir/superiso"$PID".tgz -C "$SPECTRDIR"
# fi

# Check if nmssmcalc output exists. If so, untar.
# -----------------------------------------------------------------------------
# if [ -e $hdfsdir/nmssmcalc"$PID".tgz ]; then
#     tar -xvzf $hdfsdir/nmssmcalc"$PID".tgz -C "$SPECTRDIR"
# fi

ls

# Run analysis script over files
# -----------------------------------------------------------------------------
python analyse_scans.py "$SPECTRDIR" --ID "$PID"

# Copy files to hdfs
# -----------------------------------------------------------------------------
for f in *.csv; do
    hadoop fs -copyFromLocal -f $f ${hdfsdir#/hdfs}/$(basename $f)
done

# Cleanup
# -----------------------------------------------------------------------------
rm -r $SPECTRDIR
