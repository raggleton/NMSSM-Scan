# This is the script to run to submit a new set of scan jobs
#
# 1: Edit NMSSM_scan.pl to ensure you're running the correct number of events
# per job, and over the correct parameter range
#
# 2: Edit the parameters below to run N jobs. The total number of param points
# scanned is then events per job * NJOBS
#
# 3: Optionally edit DESCRIPTION to add something descriptive to your job folder.
# By default, it just uses NJOBS.
#
# 4: Edit Proto_files/runScan.condor to make sure paths are correct
#
# Finally, run me.
#
# This will automatically create a job directory, and create and submit a
# condor job file
#

# Number of parallel jobs to run
NJOBS=10

# Make new job directory
DESCRIPTION=$NJOBS
DATE=$(date +"%d_%b_%y_%k%M")
JOBDIR="jobs_${DESCRIPTION}_${DATE}"

if [ ! -d "$JOBDIR" ]; then
    echo "Putting job files in $JOBDIR"
    mkdir $JOBDIR
else
    echo "Cannot create job folder, it already exists"
    exit 1
fi

FULLPATH=$(readlink -e $JOBDIR)
echo $FULLPATH

# Make a condor submission script
cp Proto_files/runScan.condor $JOBDIR/runScan.condor
# Need the @ instead of usual / since we're dealing with paths
sed -i "s@SEDINITIAL@$FULLPATH@g" "$JOBDIR/runScan.condor"

# args=""
# sed -i "s@SEDARG@$args@g" "$JOBDIR/runScan.condor"

JOBS="queue $NJOBS"
sed -i "s@SEDJOB@$JOBS@g" "$JOBDIR/runScan.condor"

OUTPUT="spectr0.tgz"
for i in $(eval echo "{1..$(($NJOBS-1))}"); do
    OUTPUT="$OUTPUT,spectr$i.tgz"
done
sed -i "s@SEDOUTPUT@$OUTPUT@g" "$JOBDIR/runScan.condor"


# Submit jobs
echo "Submitting jobs to condor..."
condor_submit $JOBDIR/runScan.condor